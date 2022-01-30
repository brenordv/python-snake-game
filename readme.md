# Snake Game Clone
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=bugs)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=brenordv_python-snake-game&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=brenordv_python-snake-game)

Not a full game, but a playable one.
Probably buggy... (or full of crazy features, depending on if you're a 'glass half full kind of person')

I left a lot of comments on this script to help people understand better what is happening.

## Instructions
1. You move by using the directional keys.
2. If you hold any directional key, the snake will speed up. (I'll remove this in the future.)
3. Snake will grow in size everytime you eat something.
4. If you hit yourself or the borders of the screen, game over!
5. To leave the game, press `ALT+X`
 
## Demo
[Quick video demo of this game](./python_snake_game.mp4)
# How to install
Install the dependencies using the command:
```shell
pip install -r requirements.txt
```


If you're on Windows, you also need to install the `requirements-windows.txt` file.
```shell
pip install -r requirements-windows.txt
```


# How to play
Just run the main script.

## Without logging gameplay
```shell
python snake.py
```

## Logging gameplay
```shell
python snake.py --log
```
or
```shell
python snake.py -l
```

# TODO
1. Create tests
2. Show play area borders
3. Print the name of the game
4. Print (and update) the score 