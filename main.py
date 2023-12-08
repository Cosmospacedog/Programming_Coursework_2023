'''
This Script handles the backend using flask
'''
from json import dump
from flask import render_template,request,Flask
from game_engine import attack
from components import initialise_board,create_battleships,place_battleships
from mp_game_engine import generate_attack

class WebGame:
    '''
    This class Handles The game for the backend
    '''
    def __init__ (self,size:int):
        '''
        creates a new web game of a given size
        '''
        self.winstate = None
        self.size = size
        self.ships = create_battleships()
        self.players = None
    def process_attack(self,raw_data):
        '''
        proccesses an attack from the front end and returns
        a dictionary containing the next AI move, Hit data
        and, in the case of a winning state, who the winner
        is. This function will return Nothing if the given
        coordinates have already been played.
        '''
        data = raw_data.args
        coords = (int(data.get('x')), int(data.get('y')))
        response = {}
        if coords in self.players['Player'][2]:
            print('passed')
            return None
        hitstate = self.shoot(coords,
                              'Player',
                              'AI'
                              )
        response['hit'] = hitstate
        ai_coords = self.get_ai_shot('AI')
        response['AI_Turn'] = ai_coords
        self.shoot(
            ai_coords,
            'AI',
            'Player'
            )
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
        coords,self.players[
            player
            ][2] = generate_attack(
                self.players[player][0],
                past_attacks=self.players[player][2],
                algorithm='simple'
                )
        return coords
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
