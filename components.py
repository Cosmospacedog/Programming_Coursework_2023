'''
This Module holds all major components required for the
function of the Game
'''
from random import randint
from json import load

def initialise_board(
    size=10
    ):
    '''
    Generates a board within a given scale.
    ie: initialise_board(10) will return a 10x 10 array
    '''
    board = [
        [
            None for J in range (size)
        ]
        for i in range (size)
    ]
    return board


def create_battleships(
        filename='battleships.txt'
        ):
    '''
    Returns a dictionary containing ships and their
    appropriate sizes according to a txt file.
    Filename will be set to battleships.txt by default
    '''
    with open(filename,'r+',encoding="utf-8") as raw_data:
        ship_data = [
            line.strip(
                ).split(
                    ':'
                    ) for line in raw_data
            ]
    #Obtains ship data from file by splitting lines at colon
    #and saves to an array.
    ship_dict = {}
    for line in ship_data:
        ship_dict[
            line[0]
            ] = int(
                line[1]
                )
    #saves ship data to a dictionary.
    return ship_dict

def simple_placement(board,ships):
    '''
    places each ship at the beginning of each row
    until no more ships are alliable.
    '''
    row = 0
    for ship in ships:
        for i in range(
            ships[
                ship
                ]):
            board[
                row
                ][
                    i
                    ] = ship
        row += 1
    return board

def random_placement(board,ships):
    '''
    places each ship at a random position, pointing
    in a random direction.
    '''
    for ship in ships:
        valid_directions = []

        while len(
            valid_directions
            ) == 0:
            position = (
                randint(0,len(board)-1),
                randint(0,len(board)-1)
                )
            #generate an initial random point.
            if position[0] + ships[ship] <= len(board) - 1:
                if {
                    board[
                        position[1]
                        ][i] for i in range(
                            position[0],position[0] + ships[ship]
                            )
                        } == {None}:
                    valid_directions.append(
                        'Right'
                        )
            #Checks if its valid to place the ship to the horizontally.
            if position[1] + ships[ship] <= len(board) - 1:
                if {
                    board[
                        i
                        ][position[0]] for i in range(
                            position[1],position[1] + ships[ship]
                            )
                        } == {None}:
                    valid_directions.append(
                        'Up'
                        )
            #Checks if its valid to place the ship vertically.
        if len(valid_directions) > 1:
            valid_directions.pop(
                randint(0,1)
                )
            #checks if both directions are valid and removes one at random
            #if so.
        if valid_directions[0] == 'Right':
            for i in range(
                position[0],position[0]+ ships[ship]
                ):
                board[
                    position[1]
                    ][i] = ship
            #places a ship horizontally
        else:
            for i in range(
                position[1],position[1] + ships[ship]
                ):
                board[i][
                    position[0]
                    ] = ship
            #places a ship vertically
    return board

def custom_placement(board,ships):
    '''
    Loads and uses placement options from a JSON file.
    This file is named 'placement.json' and should be
    placed in the source directory.
    '''
    with open('placement.json','r+',encoding="utf-8") as raw_data:
        data = load(raw_data)
    #Load data from json.
    for ship in data:
        if data[ship][2] == 'h':
            for i in range(
                int(data[ship][0]), int(data[ship][0])+ ships[ship]
                ):
                board[
                    int(data[ship][1])
                    ][i] = ship
        #if the ship is horizontal, place accordingly.
        else:
            for i in range(
                int(data[ship][1]),int(data[ship][1]) + ships[ship]
                ):
                board[i][
                    int(data[ship][0])
                    ] = ship
        #if the ship is vertical, place accordingly.
    return board

def place_battleships(
        board,
        ships,
        algorithm='simple'
        ):
    '''
    Places battleships on a provided array according
    to the users choice.
    '''
    options = {
        'custom':custom_placement,
        'simple':simple_placement,
        'random':random_placement,
    }
    return options[algorithm](board,ships)
