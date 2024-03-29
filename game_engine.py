'''
This module contains the code for controlling the
game backend as well as a command line GUI for
playing.
'''
import logging
from components import initialise_board,create_battleships,place_battleships

logging.basicConfig(
    filename='Battleships.log',
    filemode='a',
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s')

def attack(coordinates:tuple,
           board:list,
           battleships:dict
           ) -> (str,dict):
    '''
    Compare an input co-ordinate with a given game
    board and return a string indicating how successful
    it was.
    '''
    item_on_space = board[coordinates[1]][coordinates[0]]
    if item_on_space is not None:
        #checks if there is a ship in the space.
        battleships[
            item_on_space
            ] -= 1
        #reduce the size of the battleship in the dict
        if battleships[
            item_on_space
            ] == 0:
            #check if the ship has no more pieces
            logging.info(
                'Player sunk ship at %s',
                coordinates
            )
            return 'Sunk!',battleships
        logging.info(
                'Player hit ship at %s',
                coordinates
            )
        return 'Hit!',battleships
    logging.info(
        'Player missed at %s',
        coordinates
    )
    return 'Miss!',battleships

def cli_coordinates_input(board:list=initialise_board(10)
                          ) -> tuple:
    '''
    Receives co-ordinate inputs from a human
    via the command line.
    '''
    while True:
        try:
            coordinates = tuple(
                int(i) for i in input(
                'Please input co-ordinates separated by a comma (x,y):'
            ).split(',')
            )
            try:
                if len(board) >= coordinates[0] and len(board[0]) >= coordinates[1]:
                    #check if the coordinates are in a valid range.
                    break
                logging.error('Coordinates out of range')
            except IndexError:
                logging.error('Only one coordinate provided')
        except ValueError:
            logging.error('Invalid coordinate input')
        #Recieves and proccess coordinates.

    return coordinates

def simple_game_loop() -> None:
    '''
    A simple testing mode with no second player and
    one board using the simple placement algorithm.
    '''
    print('Welcome to the simple command line interface for battleships!')
    ships = create_battleships()
    board = place_battleships(
        initialise_board(10),
        create_battleships())
    #Create a ship and board for one player.
    while sum(
        length for ship,length in ships.items()
        ) > 0:
        #Check if there are still ships  left.
        message,ships = attack(
            cli_coordinates_input(
                board
                ),
            board,
            ships
        )
        print(message)
        #Display the performance of a shot
    print('Game Over!')

def showboard(board:list,
              past_moves:list=None
              ) -> None:
    '''
    Generate a gameboard to display in the command
    line.
    '''
    if past_moves is None:
        past_moves = []
    board = [
        [
            '   ' if column is None else ' S ' for column in row
            ]
        for row in board
        ]
    for move in past_moves:
        board[
            move[0]
            ][move[1]] = ' X '
    display_board = [
        '|'.join(row) for row in board
        ]
    print('Your Board:')
    print(f'\n{"-" * len(display_board[0])}\n'.join(display_board))
    logging.info(
        'board successfully displayed'
    )

if __name__ == '__main__':
    simple_game_loop()
