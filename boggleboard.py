# Boggle board class
"""Extends the Board class with specific features required for Boggle"""

# import modules and classes
from graphics import *
from myrandom import randint
from boggleletter import BoggleLetter
from board import Board

# global variable to represent letters that can go on a boggle cube
CUBES =   [[ "A", "A", "C", "I", "O", "T" ],
           [ "T", "Y", "A", "B", "I", "L" ],
           [ "J", "M", "O", "Qu", "A", "B"],
           [ "A", "C", "D", "E", "M", "P" ],
           [ "A", "C", "E", "L", "S", "R" ],
           [ "A", "D", "E", "N", "V", "Z" ],
           [ "A", "H", "M", "O", "R", "S" ],
           [ "B", "F", "I", "O", "R", "X" ],
           [ "D", "E", "N", "O", "S", "W" ],
           [ "D", "K", "N", "O", "T", "U" ],
           [ "E", "E", "F", "H", "I", "Y" ],
           [ "E", "G", "I", "N", "T", "V" ],
           [ "E", "G", "K", "L", "U", "Y" ],
           [ "E", "H", "I", "N", "P", "S" ],
           [ "E", "L", "P", "S", "T", "U" ],
           [ "G", "I", "L", "R", "U", "W" ]]


class BoggleBoard(Board):
    """Boggle Board class implements the functionality of a Boggle board.
    It inherits from the Board class and extends it by creating a grid
    of BoggleLetters, shaken appropriately to randomize play."""

    __slots__ = ['_grid']

    def __init__(self):
        super().__init__() # initialize attributes from parent class

        self._grid = [] # initialize grid attribute

        # initialize grid positions with BoggleLetter objects
        for cols in range(self.cols):
            colLetters = [BoggleLetter(cols, rows, '') for rows in range(self.rows)]
            self._grid.append(colLetters)

    def getLetterObj(self, pos):
        """Returns the letter object (that is, a BoggleLetter)
        at given grid position pos, a tuple of (column, row)"""
        col, row = pos                  # get grid position
        return self._grid[col][row]     # get BoggleLetter at position

    def getLetter(self, pos):
        """Returns the text (string) of the BoggleLetter
        at given position pos, a tuple of (column, row)"""
        letObj = self.getLetterObj(pos) # get BoggleLetter at position
        return letObj.letter            # get letter from BoggleLetter

    def setLetter(self, pos, alph):
        """Given grid position pos, a tuple of (column, row),
        set the text of the BoggleLetter at that position to alph (a string)"""
        letObj = self.getLetterObj(pos) # get BoggleLetter at position
        letObj.letter = alph            # set letter of BoggleLetter

    def clearLetters(self):
        """Unclicks all boggle letters on the board without changing any other attribute"""
        # traverse the grid
        for rows in range(self.rows):
            for cols in range(self.cols):
                ltr = self.getLetterObj((cols, rows)) # get BoggleLetter object
                ltr.unclick()       # unclick letter

    def reset(self):
        """Clears the boggle board by clearing letters,
        clears all text areas (right, lower, upper) on board
        and resets the letters on board by calling shakeCubes"""

        # traverse the grid and set each BoggleLetter object to an empty string
        for cols in range (self.cols):
            for rows in range(self.rows):
                bLet = self._grid[cols][rows]
                bLet.unclick()
                bLet.textObj.setText("")

        self.shakeCubes() # shake the cubes

        # clear text areas
        self.clearTextArea()
        self.clearLowerText()
        self.clearUpperText()

    def drawBoard(self, win):
        """Draws the boggle board with all the letters on it.
        Overrides inherited drawBoard method of super class"""
        super().drawBoard(win) # call drawBoard from the parent class

        # traverse the grid and 'draw' each BoggleLetter object
        for cols in range(self.cols):
            for rows in range(self.rows):
                bLet = self._grid[cols][rows]
                bLet.textObj.draw(win)

    def shakeCubes(self):
        """Shakes the boggle board and sets letters
        as described by the handout."""
        count = 0 # initialize

        # traverse the grid
        for rows in range(self.rows):
            for cols in range(self.cols):

                # randomize cube and side number
                cubeNumber = randint(0, self.rows * self.cols - 1 - count)
                sideNumber = randint(0, 5)

                # set grid letter from randomly selected cube side
                letter = CUBES[cubeNumber][sideNumber]
                self.setLetter((cols, rows), letter)

                # swap rows to avoid reusing cube
                temp = CUBES[cubeNumber]
                CUBES[cubeNumber] = CUBES[15 - count]
                CUBES[15 - count] = temp

                # update count
                count = count + 1

    def __str__(self):
        """ Returns a string representation of this BoggleBoard """
        board = ''
        for c in range(self.cols):
            for r in range(self.rows):
                color = self.getLetterObj((c,r)).color
                letter = self.getLetter((c,r))
                board += '[{}:{}] '.format(letter,color)
            board += '\n'
        return board


if __name__ == "__main__":
    win = GraphWin("Boggle", 400, 400)
    board = BoggleBoard()
    board.reset()
    board.drawBoard(win)

    exit = False
    while not exit:
        pt = win.getMouse()
        if board.inExit(pt):
            exit = True
        else:
            position = board.getPosition((pt.getX(), pt.getY()))
            print("{} at {}".format(board.getLetter(position), position))
