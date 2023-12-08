'''
This module controls an automated player and runs
a simple command-liine game against them when ran as
main
'''
from random import randint
from components import initialise_board,create_battleships,place_battleships
from game_engine import cli_coordinates_input,showboard,attack

def simple_attack(
    past_attacks:list,
    board:list
    ):
    '''
    Generate a simple attack at a random
    position
    '''
    command = (randint(0,len(board) -1),
               randint(0, len(board) - 1)
               )
    #Generate a random shot.
    while command in past_attacks:
        #check if the shot has been used before and get
        #a new one if so
        command = (randint(0,len(board) -1),
                   randint(0,len(board) -1)
                   )
    past_attacks.append(command)
    return command,past_attacks

def generate_attack(
        board:list=initialise_board(10),
        past_attacks:list=None,
        algorithm:str='simple'
        ):
    '''
    Return a choice of shot based on a given algorithm.
    '''
    if past_attacks is None:
        past_attacks = []
    options = {
        'simple':simple_attack
    }
    return options[algorithm](past_attacks,board)


def ai_opponent_game_loop(names=('player1','AI')):
    '''
    Creates A basic game loop using a simple command line gui
    and the random Ai playstyle.
    '''
    print('Welcome to the simple AI command line interface for battleships!')
    ships = create_battleships()
    players[names[0]] = [
        place_battleships(
            initialise_board(10),
            ships,
            algorithm='custom'
        ),
        create_battleships(),
        'Human',
        []
    ]
    players[names[1]] = [
        place_battleships(
            initialise_board(10),
            create_battleships(),
            algorithm='random'
        ),
        ships,
        'AI',
        []
    ]
    winner = None
    while winner is None:
        for i in range(0,2):
            if players[
                names[i]
                ][2] == 'AI':
                command,players[
                    names[i]][3] = generate_attack(
                            players[
                                names[i - 1]][0],
                            players[
                                names[i]][3],
                                )
            if players[
                names[i]
                ][2] == 'Human':
                showboard(
                    players[
                        names[i]][0],
                    past_moves=players[
                        names[i - 1]
                        ][3])
                command = cli_coordinates_input(
                    players[
                        names[i - 1]
                        ][0])[::-1]
            message,players[
                    names[i - 1]
                    ][1] = attack(
                        command,
                        players[
                            names[i - 1]
                            ][0],
                        players[
                            names[i - 1]
                            ][1])
            print(f'{names[i]} - {message}')

            if sum(
                players[names[i - 1]][1][ship] for ship in players[names[i - 1]][1]
                ) ==0:
                winner = names[i]
    print(winner)

players = {}

if __name__ == '__main__':
    ai_opponent_game_loop()
