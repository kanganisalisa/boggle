# script game.py
"""Implements the logic of the game of boggle."""

# import all relevant packages and classes
from graphics import *
from random import randint
from boggleboard import BoggleBoard
from boggleletter import BoggleLetter
from bogglewords import BoggleWords
import time

# This helper function creates the Boggle lexicon.
def lexicon(filename='bogwords.txt'):
    """Reads words (one per line) from filename (by default 'bogwords.txt')
    and returns a set of all words"""
    result = set()
    with open(filename) as f:
        for lines in f:
            result.add(lines.strip())
    return result

def setup(win, board):
    """Given a graphical window and BoggleBoard board,
    sets up the game board by resetting the letters on it
    and drawing the board with letters"""
    board.reset()           # reset board
    board.drawBoard(win)    # draw  board

def resetLower(board):
    """Given a BoggleBoard board, clears the letters on the board,
    along with the lower text area"""
    board.clearLetters()        # clear letters
    board.clearLowerText()      # clear lower text

def update(board, bWords):
    """Updates the state of the BoggleBoard board after a valid word has been found
    and added to BoggleWords bWords; updates right text area, clears lower
    text area, and resets BoggleLetters to unclicked state."""
    board.setTextArea(bWords._allWords) # set right text to all valid words
    board.clearLowerText()              # clear lower text
    board.clearLetters()                # unlick all boggle letters
    bWords.clearCurrentWord()           # reset current word

def play(win, board):
    """Given a graphical window and a BoggleBoard board, implements the logic
    for playing the game"""

    # initialize flag and boggle words
    exitFlag = False

    # populate the lexicon
    validWords = lexicon()

    # initialize an empty BoggleWords object
    bWord = BoggleWords()

    # game directions for user
    board.setStringToUpperText('Click to Start Timer')

    # wait to get mouse click
    pt = win.getMouse()

    # intialize time
    seconds = 31
    start = time.time()

    # intialize score
    score = 0

    while not exitFlag:

        pt = None

        # timer
        currTime = time.time()
        diff = currTime - start
        timeLeft = int(seconds - diff)
        timer = 'Countdown: {} Current Score: {}'.format(str(timeLeft), score)
        board.setStringToUpperText(timer)
        time.sleep(.1)

        # find (col, row) coord of mouse click
        pt = win.checkMouse()

        # if timer runs out
        while timeLeft <= 0:
            numWords = len(bWord._wordSet) # number of words found by user
            board.setStringToUpperText('Times Up! Words Found: {} Final Score: {}'.format(numWords, score))
            board.clearLowerText()

            # wait to get mouse click
            pt = win.getMouse()

            if pt:
                if board.inExit(pt): # exit
                    exitFlag = True
                    break
                elif board.inReset(pt): # reset board and timer
                    bWord.reset()
                    board.reset()
                    start = time.time()
                    score = 0
                    pt = None
                    break

        if not pt:
            continue

        # get mouse location
        position = board.getPosition((pt.getX(), pt.getY()))

        # step 1: check for exit button and exit
        if board.inExit(pt):
            exitFlag = True

        # step 2: check for reset button and reset
        if board.inReset(pt):
            bWord.reset()
            board.reset()
            start = time.time()
            score = 0

        # step 3: check if click is on a cell in the grid
        if board.inGrid(pt):

            # get BoggleLetter at that position and change color to blue
            bLetter = board.getLetterObj(position)
            bLetter.click()

            # if starting a new word, add letter and display it on lower text of board
            if bWord.currWord == []:
                bWord.addLetter(bLetter)
                board.setStringToLowerText(bLetter.letter)

            # if adding letter to existing word, check for adjacency, update state
            elif bLetter.isAdjacent(bWord.currWord[-1]):
                bWord.addLetter(bLetter)
                board.addStringToLowerText(bLetter.letter)

            # if clicked on same letter as last time, end word, check for validity
            elif bLetter == bWord.currWord[-1]:
                if bWord.wordStr.lower() in validWords: # if word is valid update bWords
                    bWord.addWord()

                    wordLen = len(bWord.wordStr) # length of valid word

                    # update corresponding boggle score
                    if wordLen <= 4:
                        score = score + 1
                    elif wordLen == 5:
                        score = score + 2
                    elif wordLen == 6:
                        score = score + 3
                    elif wordLen == 7:
                        score = score + 5
                    else:
                        score = score + 11

                    # update board
                    update(board, bWord)

                update(board, bWord)

            # if clicked on some other letter, cancel word, reset stat
            else:
                resetLower(board)

if __name__ == '__main__':
    win = GraphWin("Boggle", 400, 400)
    board = BoggleBoard()
    setup(win, board)
    play(win, board)
