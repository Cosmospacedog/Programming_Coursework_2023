'''
This Script handles the backend using flask
'''
import logging
from json import dump
from flask import render_template,request,Flask
from game_engine import attack
from components import initialise_board,create_battleships,place_battleships
from mp_game_engine import generate_attack
from battleships_ai import AIPlayer
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
        self.aiplayer = AIPlayer(size)
        self.winstate = None
        self.size = size
        self.ships = create_battleships()
        self.players = None  
        self.algorithm = algorothm

    def shoot(self,coords:tuple,player:str,target:str):
        '''
        Processes an attack on a given target's board,
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
        #append coordinates to the shot log
        self.players[player][2].append(coords)
        if message != 'Miss!':
            return True
        return False
    def get_ai_shot(self,player:str):
        '''
        Generates an attack based on previous hit data.
        '''
        if self.algorithm == 'simple':
            #returns a random shot if the algorithm is set
            #to simple
            coords,self.players[
                player
                ][2] = generate_attack(
                    self.players[player][0],
                    past_attacks=self.players[player][2],
                    algorithm='simple'
                    )
            return coords
        if self.algorithm == 'complex':
            #gets a predicted shot if the algorithm is set to
            #complex
            return self.aiplayer.attack()
        logging.error('Invalid algorithm %s',self.algorithm)
        return None
    def check_winner(self):
        '''
        Checks to see if there are any players with no
        ships left, and if so returns a winner.
        '''
        #checks to see if any players have ships with values
        #greater than 0
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
        #sets all values changed since initialization
        #to their starting points
        self.aiplayer = AIPlayer(self.size)
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
    Processes requests from the placement webpage
    and dumps them to file.
    '''
    #opens a json file and makes data dump
    with open('placement.json','w',encoding="utf-8") as data:
        dump(raw_data.json,data)
        return {}
#change value to set size and algorithm
GAME = WebGame(10)

app = Flask(__name__)

@app.route('/placement')
def placement_interface(methods=['POST','GET']):
    '''
    Render the ship placement template with appropriate
    paramiters.
    '''
    #When a placement url is requested, push the appropriate webpage
    return render_template('shipPlacement.html',board_size = GAME.size,ships = GAME.ships)

@app.route('/', methods=['POST','GET'])
def root():
    '''
    Set the main page to the main template, initialise a game
    and render appropriately.
    '''
    #When the root url is refreshed or requested, refresh the
    #game object and push the homepage
    GAME.newgame()
    return render_template('main.html',player_board=GAME.players['Player'][0])

@app.route('/<request_id>', methods=['POST','GET'])
def process(request_id):
    '''
    process requests with the appropriate method
    '''
    #Select an option based on the type of request
    #made
    logging.info('Got request: %s',request_id)
    options = {
        'attack':GAME.process_attack,
        'placement':process_placement
    }
    return options[request_id](request)

if __name__ == "__main__":
    #Initialize the app if the script is run as main
    app.run()
