
# ECM1400 Coursework - Battleships

This is my coursework for the 2023 ECM1400 programming module.  

This Readme is written in sphinx markdown and requires a proper interpreter to read.

## Demo


![Alt Text](https://i.imgur.com/klWOMwY.gif)
## Installation

Compatible with python 3.7+  

Packeges Used:
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

4 weeks post deadline, installation will be avaliable via:
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
When The flask app is run, it will typically be hosted at http://127.0.0.1:5000/ unless flask says otherwise in console.  

In order to Configure ship placement,open http://127.0.0.1:5000/placement, this will load the placement screen and allow you to place ships with default size.

![App Screenshot](https://imgur.com/Kq63FMI.png)  

After placing Ships and selecting the 'Send Game' Button you willl be redirected  to the main page, where you can play the game.

![App Screenshot](https://imgur.com/IncxVqK.png)
## License

[MIT](https://choosealicense.com/licenses/mit/)

