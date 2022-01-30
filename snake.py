# -*- coding: utf-8 -*-
import argparse
import random
import curses
from enum import Enum
from operator import itemgetter

from raccoon_simple_stopwatch.stopwatch import StopWatch
from simple_log_factory.log_factory import log_factory


class Direction(Enum):
    Right = 1
    Left = 2
    Up = 3
    Down = 4


def _init_screen(timeout):
    # Initializes screen
    screen = curses.initscr()

    # Hides the cursor
    curses.curs_set(0)

    # Gets the height and width of the screen
    height, width = screen.getmaxyx()

    # Creates a new windows
    window = curses.newwin(height, width, 0, 0)

    # Enables keypad
    window.keypad(True)

    # Refresh rate
    window.timeout(timeout)

    return {
        "screen": screen,
        "height": height,
        "width": width,
        "window": window
    }


def _get_initial_position(height, width):
    x = int(width / 4)
    y = int(height / 4)
    return x, y


def _create_snake(x, y, num_parts, direction: Direction):
    snake = []

    if direction == Direction.Left:
        diff_x = -1
        diff_y = 0
    elif direction == Direction.Right:
        diff_x = 1
        diff_y = 0
    elif direction == Direction.Up:
        diff_x = 0
        diff_y = -1
    else:
        # Direction.Down
        diff_x = 0
        diff_y = 1

    for i in range(num_parts):
        snake.append([y + (diff_y * (i + 1)), x + diff_x * (i + 1)])

    return snake


def _create_food(height, width, snake):
    while True:
        new_food = [
            random.randint(1, height - 1),
            random.randint(1, width - 1)
        ]
        if new_food in snake:
            continue

        return new_food


def _add_food_to_screen(food, window):
    window.addch(int(food[0]), int(food[1]), curses.ACS_LANTERN)


def _get_initial_key(direction: Direction):
    if direction == Direction.Left:
        return curses.KEY_LEFT

    elif direction == Direction.Right:
        return curses.KEY_RIGHT

    elif direction == Direction.Up:
        return curses.KEY_UP

    return curses.KEY_DOWN


def _get_pressed_key(window, current_key):
    next_key = window.getch()

    if current_key == curses.KEY_UP and next_key == curses.KEY_DOWN or \
            current_key == curses.KEY_DOWN and next_key == curses.KEY_UP or \
            current_key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT or \
            current_key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT or \
            next_key == -1:
        return current_key

    return next_key


def _has_hit_boundaries(height, width, snake):
    return snake[0][0] in [0, height] or snake[0][1] in [0, width]


def _has_hit_itself(snake):
    return snake[0] in snake[2:]


def _update_snake(snake, key):
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)
    return snake


def _has_hit_food(snake, food):
    return snake[0] == food


def _make_snake_grow(snake):
    """get your mind out of the gutter! ;)"""
    snake.insert(0, snake[0])
    return snake


def _clear_window_position(window, pos):
    window.addch(pos[0], pos[1], ' ')


def _paint_snake_head(snake, window):
    try:
        window.addch(snake[0][0], snake[0][1], curses.ACS_BLOCK)
    except curses.error:
        pass


def _change_timeout(window, current_timeout, min_timeout=10, timeout_diff=5):
    t = current_timeout - timeout_diff
    if t < min_timeout:
        return current_timeout

    window.timeout(t)
    return t


def _print_game_over(score, snake, sw):
    print(f"######################## Game Over! #############################")
    print(f"Score: {score:010d}")
    print(f"Snake size: {len(snake)}")
    print(f"Time playing: {sw.end()}")
    print(f"#################################################################")


def _log(log_func, message, should_log):
    if not should_log:
        return
    log_func(message)


def main_snake(log_gameplay: bool, num_parts: int = 3,
               score_per_food: int = 1, initial_direction: Direction = Direction.Right):
    # Score.
    score = 0

    # Number of loops.
    loop = 0

    # Initial timeout. The higher, the easier the game is.
    timeout = 500

    # Initializing logging.
    if log_gameplay:
        logger = log_factory(log_name="SNAKE", log_file="./snake.log") if log_gameplay else None
        log_info = logger.info
        log_exception = logger.exception

    else:
        log_info = None
        log_exception = None

    # Initializing stopwatch.
    sw = StopWatch(auto_start=True)

    # Initialize curses screen.
    screen_config = _init_screen(timeout=timeout)

    # To make things easier, will deconstruct screen_config variable.
    screen, height, width, window = itemgetter("screen", "height", "width", "window")(screen_config)

    # Getting initial X and Y position.
    initial_x, initial_y = _get_initial_position(height=height, width=width)

    # Creates the snake objects (one X and Y for each section of the snake).
    snake = _create_snake(x=initial_x, y=initial_y, num_parts=num_parts, direction=initial_direction)

    # Creates a food item.
    initial_food = _create_food(height=height, width=width, snake=snake)

    # Adds the food to the screen.
    _add_food_to_screen(food=initial_food, window=window)

    # Considering the initial direction, gets the respective (directional) key.
    key = _get_initial_key(initial_direction)

    try:
        _log(log_info, "Game starting!", log_gameplay)

        food = initial_food

        _log(log_info, f"Initial food @: {food}", log_gameplay)
        _log(log_info, f"Initial snake: {snake}", log_gameplay)

        # Game loop
        while True:
            # Gets which key is/was pressed
            key = _get_pressed_key(window, key)

            if key == curses.ALT_X:
                raise InterruptedError()

            # Add 1 to the loop count. For now, it is used only to check whether to check for self collision or not.
            # TODO: Find a better way to do this.
            loop = loop + 1 if loop <= num_parts else loop

            # Do the collision checks
            # Has the snake collided with game play area?
            hit_boundaries = _has_hit_boundaries(height=height, width=width, snake=snake)

            # Has the snake collided with game itself?
            hit_self = loop > num_parts and _has_hit_itself(snake=snake)

            # If there was any collision, then game over...
            if hit_boundaries or hit_self:
                _log(log_info, f"Hit something! Boundaries: {hit_boundaries} | Self: {hit_self}", log_gameplay)
                curses.endwin()
                quit()

            # Update snake object, so it can appear to be moving around the screen...
            snake = _update_snake(snake=snake, key=key)

            # If the snake hits the food...
            if _has_hit_food(snake=snake, food=food):
                # Increment the score
                score += score_per_food

                # Change the snake size
                snake = _make_snake_grow(snake=snake)

                _log(log_info,
                     f"Got food! Score now is '{score}' and snake now has a size of '{len(snake)}'.",
                     log_gameplay)

                # Creates another food, somewhere in the game play area
                food = _create_food(height=height, width=width, snake=snake)

                _log(log_info, f"Next food will be placed @ {food}", log_gameplay)

                # And adds it to the screen.
                _add_food_to_screen(food=food, window=window)

                # Every time we have an even score, the difficulty is increased.
                if divmod(score, 2)[1] == 0:
                    timeout = _change_timeout(window=window, current_timeout=timeout)

            else:
                # Updates snake on screen, removing last tail block.
                tail = snake.pop()
                _clear_window_position(window=window, pos=tail)

            # Paints the head of the snake for this "frame"
            _paint_snake_head(snake, window)

    except InterruptedError:
        curses.endwin()
        _log(log_info, "User quit!", log_gameplay)

    except Exception as e:
        _log(log_exception, e, log_gameplay)

    finally:
        _log(log_info, f"Game Over! Final score: {score} | Final snake size: {len(snake)}", log_gameplay)
        _log(log_info, f"Loops: {loop}", log_gameplay)
        _log(log_info, f"Time played: {sw.elapsed()}", log_gameplay)
        _print_game_over(score, snake=snake, sw=sw)

    quit()


def main():
    parser = argparse.ArgumentParser(description="Find text in files.")

    parser.add_argument("--log", "-l",
                        default=False,
                        dest="log",
                        action="store_true",
                        help="When used, will create a log file for the game play. (Default: false)")

    args = parser.parse_args()
    main_snake(log_gameplay=args.log)


if __name__ == '__main__':
    main()
