'''
This Script handles the backend using flask
'''
import logging
from json import dump
from flask import render_template,request,Flask
from game_engine import attack
from components import initialise_board,create_battleships,place_battleships
from mp_game_engine import generate_attack
import Battleships_ai
#Configure Logs to go to file
logging.basicConfig(
    filename='Battleships.log',
    filemode='a',
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s')

class WebGame:
    '''
    This class Handles The game for the backend
    '''
    def __init__ (self,size:int,algorothm = 'complex') -> None:
        '''
        creates a new web game of a given size
        '''
        #initialise necessary values and create player instances
        self.aiplayer = Battleships_ai.AI_Player(10)
        self.winstate = None
        self.size = size
        self.ships = create_battleships()
        self.players = None  
        self.algorithm = algorothm
    def process_attack(self,raw_data):
        '''
        proccesses an attack from the front end and returns
        a dictionary containing the next AI move, Hit data
        and, in the case of a winning state, who the winner
        is. This function will return Nothing if the given
        coordinates have already been played.
        '''
        #get request arguments and extract necessary values
        data = raw_data.args
        coords = (int(data.get('x')), int(data.get('y')))
        response = {}
        #check if the square has been played before, and
        #if so do nothing
        if coords in self.players['Player'][2]:
            return None
        #get the success of the player's shot
        hitstate = self.shoot(coords,
                              'Player',
                              'AI'
                              )
        response['hit'] = hitstate
        #request a shot from the AI
        ai_coords = self.get_ai_shot('AI')
        response['AI_Turn'] = ai_coords
        aihitstate = self.shoot(
                ai_coords,
                'AI',
                'Player'
                )
        #tells the AI the success of its shot
        if aihitstate:
            self.aiplayer.proccessattack(ai_coords[0],ai_coords[1],1)
        else:
            self.aiplayer.proccessattack(ai_coords[0],ai_coords[1],-1)
        self.winstate = self.check_winner()
        if self.winstate is not None:
            response['finished'] = f"{self.winstate} Wins!"
        return response
    def shoot(self,coords:tuple,player:str,target:str):
        '''
        Proccesses an attack on a given target's board,
        and stores the initial coordinates in the players
        past attack array.
        '''
        message,self.players[
            target
            ][1] = attack(
                coords,
                self.players[target][0],
                self.players[target][1]
                )
        self.players[player][2].append(coords)
        if message != 'Miss!':
            return True
        return False
    def get_ai_shot(self,player:str):
        '''
        Generates an attack based on previous hit data.
        '''
        if self.algorithm == 'simple':
            coords,self.players[
                player
                ][2] = generate_attack(
                    self.players[player][0],
                    past_attacks=self.players[player][2],
                    algorithm='simple'
                    )
            return coords
        if self.algorithm == 'complex':
            return self.aiplayer.attack()
        logging.error('Invalid algorithm %s',self.algorithm)
        return None
    def check_winner(self):
        '''
        Checks to see if there are any players with no
        ships left, and if so returns a winner.
        '''
        for player_name,player_data in self.players.items():
            if sum(
                shiplength for ship,shiplength in player_data[1].items()
            ) == 0:
                for player in self.players:
                    if player != player_name:
                        return player
        return None
    def newgame(self):
        '''
        Generates a new game when the page is refreshed.
        '''
        self.aiplayer = Battleships_ai.AI_Player(10)
        self.winstate = None
        self.players = {
            'Player':[
                place_battleships(initialise_board(self.size),
                                  self.ships,
                                  algorithm='custom'
                                  ),
                create_battleships(),
                [],
                'human'
            ],
            'AI':[
                place_battleships(initialise_board(self.size),
                                  self.ships,
                                  algorithm='random'
                                  ),
                create_battleships(),
                [],
                'random'
            ]
        }

def process_placement(raw_data):
    '''
    Proccesses requests from the placement webpage
    and dumps them to file.
    '''
    with open('placement.json','w',encoding="utf-8") as data:
        dump(raw_data.json,data)
        return {}

GAME = WebGame(10)

app = Flask(__name__)

@app.route('/placement')
def placement_interface():
    '''
    Render the ship placement template with appropriate
    paramiters.
    '''
    return render_template('shipPlacement.html',board_size = GAME.size,ships = GAME.ships)

@app.route('/', methods=['POST','GET'])
def root():
    '''
    Set the main page to the main template, initialise a game
    and render appropriatley.
    '''
    GAME.newgame()
    return render_template('main.html',player_board=GAME.players['Player'][0])

@app.route('/<request_id>', methods=['POST','GET'])
def process(request_id):
    '''
    process requests with the appropriate method
    '''
    options = {
        'attack':GAME.process_attack,
        'placement':process_placement
    }
    return options[request_id](request)

if __name__ == "__main__":
    app.run()
