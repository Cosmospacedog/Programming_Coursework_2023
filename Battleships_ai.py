from components import *
from numpy import array
class AI_Player:
    def __init__(self,size) -> None:
        self.board = initialise_board(size)
        self.size = size
        self.bounds = size-1
        self.options_board = [[0 for i in range(0,size)]
                              for j in range(0,size)]
        self.ships = create_battleships()
        self.validmove = {
            'vertical':self.checkvertical,
            'horizontal':self.checkhorizontal
        }
        self.updateoptions = {
            'vertical':self.placevertical,
            'horizontal':self.placehorizontal
        }
        self.previousattack = ()
        self.mode = 'search'
        self.destroylocation = (-1,-1)
    def attack(self):
        return self.makeshot()

    def getmax(self):
        bestscore = -1
        bestmove = (-1,-1)
        for i,row in enumerate(self.options_board):
            for j,value in enumerate(row):
                if (value > bestscore) and (self.polaritycheck(i,j) and self.board[i][j] is None):
                    bestmove = (i,j)
                    bestscore = value
        return bestmove,bestscore
    def proccessattack(self,y,x,success):
        self.board[y][x] = success
        if self.mode == 'search' and success ==1:
            self.mode = 'destroy'
            self.destroylocation = (y,x)
        print(self.mode)    
    def get_positions(self,ship):
        for i,row in enumerate(self.board):
            for j,column in enumerate(row):
                for direction in ['vertical','horizontal']:
                    if self.validmove[direction](i,j,ship):
                        self.updateoptions[direction](i,j,ship)
    
    def generateoptions(self):
        for ship,length in self.ships.items():
            self.get_positions(length)
        for row in self.options_board:
            print(f'{row}') 
        return self.options_board
    
    def checkvertical(self,y,x,ship):
        if self.mode == 'destroy':
            if not (self.destroylocation[0] in range(y,y+ship) and self.destroylocation[1] == x):
                return False
        if y + ship - 1> self.bounds:
            return False
        elif -1 in {self.board[i][x] for i in range(y,y+ship)}:
            return False
        return True
    
    def checkhorizontal(self,y,x,ship):
        if self.mode == 'destroy':
            if not (self.destroylocation[1] in range(x,x+ship) and self.destroylocation[0] == y):
                return False
        if x + ship - 1 > self.bounds:
            return False
        elif -1 in {self.board[y][i] for i in range(x,x+ship)}:
            return False
        return True
    
    def placevertical(self,y,x,ship):
        for i in range(y,y + ship):
            self.options_board[i][x] += 1
    def placehorizontal(self,y,x,ship):
        for i in range(x,x + ship):
            self.options_board[y][i] += 1
    
    def makeshot(self):
        self.generateoptions()
        bestmove,bestscore = self.getmax()
        if bestscore == 0:
            self.mode = 'search'
            self.generateoptions()
            bestmove,bestscore = self.getmax()
        self.options_board = [[0 for i in range(0,self.size)]
                              for j in range(0,self.size)]
        return bestmove
    def polaritycheck(self,y,x):
        if self.mode == 'destroy':
            return True
        if not None in set(array(self.board).flatten()[::2]):
            return True
        return (x + y) % 2 == 0