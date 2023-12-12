
# ECM1400 Coursework - Battleships

This is my coursework for the 2023 ECM1400 programming module.  

This Readme is written in markdown and is designed to be viewed in github or an appropriate interpreter.

## Demo


![Alt Text](https://i.imgur.com/klWOMwY.gif)
## Installation

Compatible with python 3.7+  

Packages Used:
- flask
- numpy
- PyTest

Setup using a conda virtual environment:
```bash
  conda create --name battleships_env python=3.7
  conda activate battleships_env
  pip install numpy flask pytest
```
Or with Python installed to path:
```bash
  pip install numpy flask pytest
```

4 weeks post deadline, installation will be available via:
```bash
  pip install git+https://github.com/Cosmospacedog/Programming_Coursework_2023.git
```
However until then the repo will remain private, and the user should just run a clone of the source code directly.
## Usage
The simple_game_loop mode can be run either by running 'game_engine.py' directly, or importing game_engine and running eg:
```python
from game_engine import simple_game_loop 

simple_game_loop()
```
The ai_opponent_game_loop mode can be run by running 'mp_game_engine.py' directly or importing it from mp_game_engine eg:
```python
from mp_game_engine import ai_opponent_game_loop 

ai_opponent_game_loop()
```
The web interface can be ran via opening the file 'main.py' or by importing the app variable from main eg:
```python
from main import app 

app.run()
```
In order to configure the web environment, you may pass in a board size or ai algorithm by editing the initialization of WebGame on line 166 of 'main.py'. By default it takes one argument 'size', but you can pass in the additional argument algorithm, set to either 'simple' or 'complex' eg:
```python
GAME = WebGame(10,algorithm='simple')
```

## Operating the Web Interface
When The flask app is run, it will typically be hosted at http://127.0.0.1:5000/, however if not, the host adress will be ouotputted to the log.  

In order to Configure ship placement,open http://127.0.0.1:5000/placement, this will load the placement screen and allow you to place ships with default size.

![App Screenshot](https://imgur.com/Kq63FMI.png)  

After placing Ships and selecting the 'Send Game' Button you will be redirected  to the main page, where you can play the game.

![App Screenshot](https://imgur.com/IncxVqK.png)
## Manual Ship Configuration
Ship data  is stored as plaintext in the file 'battleships.txt'. Its formatting follows this structure:
```
  Ship1:length1
  ship2:length2
```
Placement data is stored in JSON formatting in the file 'placement.json'. Its formatting follows this structure:
```json
  {"Ship1":["y","x","h"],"Ship2":["y","x","v"]}
```
where x and y are the starting co-ordinates of each ship, and h or v represent weather or not it is placed  vertically or horizontally.

## AI Operation

The complex AI player is controlled by the battleships_ai module. It operates via the SPD algorithm. This means it generates all of the viable ship positions on a given board, and finds the square where they most  overlap.  

Initially the AI begins in searching mode, where it searches the entire board. However, once it obtains a hit, it enters destroy mode, and only searches for configurations which include the hit space. Once there are no more combinations that align with the space that have not been hit, it returns to search mode.

Additionally, the AI considers hit polarity while searching. This allows the AI to search twice as fast as you only need consider half of the squares on board when searching, due to the fact that at least one square of each ship will appear in squares of one polarity. This feature is disengaged once destroy mode is enabled.

To generate an attack use the 'attack' function eg:
```python
from battleships_ai AIPlayer

player = AIPlayer(10)
print (player.attack())
```

Then update the model based on the response, with either a value of 1 for a 'hit' or -1 for a 'miss', using the 'proccessattack' function eg:
```python
player.proccessattack(y,x,1)
```
where y and x are the coordinates of the attack
## Provided Testing
Tests written using pytest can be found in the 'Tests' folder.If you are using an IDE such as VSC, or pycharm, the IDE will be able to automatically configure to run these tests.  

The 'Test Attack Exists' section of the main script will fail testing due to the fact that it is written in a class-based style, if you edit the test to change its scope to main.WebApp it will work fine.
## Adittional Testing
Additional tests to check the AI player module is functioning correctly can be found in the file 'test_ai.py' in the tests folder.

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- Python Backend, Additional Testing - Alex Burnett 

- Provided Testing Functions, Html Templates - The University of Exeter, Billy Thornton, Matt Collison