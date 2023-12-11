'''
This Module Handles the complex AI player.
Modes are Computed via the SPD algorithm
which computes all possible positions
and selects the most probable
'''
import logging
from numpy import array
from components import initialise_board,create_battleships
logging.basicConfig(
    filename='Battleships.log',
    filemode='a',
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s')

class AIPlayer:
    '''
    This class manages all functions
    of the AI player
    '''
    def __init__(self,size:int = 10) -> None:
        '''
        Initialize a new AI player that operates
        on a board of preset size.
        '''
        #make a new blank board
        self.board = initialise_board(size)
        self.size = size
        #create the options board, this will map
        #probabilities
        self.probability = [[0 for i in range(0,size)]
                              for j in range(0,size)]
        self.ships = create_battleships()
        #define move options
        self.validmove = {
            'vertical':self.checkvertical,
            'horizontal':self.checkhorizontal
        }
        self.updateoptions = {
            'vertical':self.placevertical,
            'horizontal':self.placehorizontal
        }
        #set the initial mode to search
        #as it will not know any locations
        self.mode = ['search',(-1,-1)]

    def getmax(self) -> (tuple,int):
        '''
        finds the square with the most possible
        ship placements on it
        '''
        bestscore = -1
        bestmove = (-1,-1)
        for i,row in enumerate(self.probability):
            for j,value in enumerate(row):
                if (
                    value > bestscore
                    ) and (
                        #Check the polarity of the chosen square
                        self.polaritycheck(
                            i,
                            j
                            #check if the square hasn't been shot
                            #yet
                            ) and self.board[i][j] is None
                        ):
                    bestmove = (i,j)
                    bestscore = value
        return bestmove,bestscore
    def proccessattack(self,y_coords,x_coords,success):
        '''
        process the result of a shot and
        check if a change of mode is 
        required
        '''
        self.board[y_coords][x_coords] = success
        if self.mode[0] == 'search' and success ==1:
            #if it was searching before and made a
            #successful hit, begin refining attacks
            logging.info('AI switching to destroy mode')
            self.mode[0] = 'destroy'
            self.mode[1] = (y_coords,x_coords)
    def get_positions(self,ship):
        '''
        get all valid positions on the board for a single ship
        '''
        for i,row in enumerate(self.board):
            for j in range (len(row)):
                for direction in ['vertical','horizontal']:
                    if self.validmove[direction](i,j,ship):
                        self.updateoptions[direction](i,j,ship)
    def generateoptions(self):
        '''
        updates the option board with all possible ship locations
        '''
        for _, length in self.ships.items():
            self.get_positions(length)
        return self.probability
    def checkvertical(self,y_coords,x_coords,ship):
        '''
        Checks to see if the ship position
        is valid if directed vertically
        '''
        if self.mode[0] == 'destroy':
            #If in destroy mode, make it impossible
            #if the permutation does not contain
            #target coords
            if not (
                self.mode[1][0] in range(
                    y_coords,
                    y_coords+ship
                    ) and self.mode[1][1] == x_coords
                ):
                return False
        #check if its out of bounds
        if y_coords + ship > self.size:
            return False
        #check if it clashes with a miss
        if -1 in {
            self.board[i][x_coords] for i in range(
                y_coords,
                y_coords+ship
                )}:
            return False
        return True
    def checkhorizontal(self,y_coords,x_coords,ship):
        '''
        Checks to see if the ship position
        is valid if directed vertically
        '''
        if self.mode[0] == 'destroy':
            #If in destroy mode, make it impossible
            #if the permutation does not contain
            #target coords
            if not (
                self.mode[1][1] in range(
                    x_coords,
                    x_coords+ship
                    ) and self.mode[1][0] == y_coords
                ):
                return False
        #check if its out of bounds
        if x_coords + ship  > self.size:
            return False
        #check if it clashes with a miss
        if -1 in {
            self.board[y_coords][i] for i in range(
                x_coords,
                x_coords+ship
                )}:
            return False
        return True
    def placevertical(self,y_coords,x_coords,ship):
        '''
        Update the probability board with a vertical
        placement
        '''
        for i in range(y_coords,y_coords + ship):
            self.probability[i][x_coords] += 1
    def placehorizontal(self,y_coords,x_coords,ship):
        '''
        Update the probability board with a Horizontal
        placement
        '''
        for i in range(x_coords,x_coords + ship):
            self.probability[y_coords][i] += 1
    def attack(self):
        '''
        Generate an attack
        '''
        #create an option map
        self.generateoptions()
        #find the most likley position
        bestmove,bestscore = self.getmax()
        if bestscore == 0:
            #if there are no possible options
            #disengage destroy mode and try
            #again
            self.mode[0] = 'search'
            self.generateoptions()
            bestmove,bestscore = self.getmax()
        #reset the options board
        self.probability = [[0 for i in range(0,self.size)]
                              for j in range(0,self.size)]
        return bestmove
    def polaritycheck(self,y_coords,x_coords):
        '''
        Check if a move has correct polarity
        This as done only every other square
        need be searched as at least one square
        of each ship will be encountered
        '''
        if self.mode[0] == 'destroy':
            #automatically pass the check in destroy
            #mode
            return True
        if not None in set(array(self.board).flatten()[::2]):
            #if there are no available squares with polarity,
            #pass automatically
            return True
        return (x_coords + y_coords) % 2 == 0
