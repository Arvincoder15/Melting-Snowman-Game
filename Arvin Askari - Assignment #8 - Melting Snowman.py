############################################################################
## File Name: Arvin Askari - Assignment #8 - Melting Snowman.py
## Program: Assignment #8 - Melting Snowman
## Author: Arvin Askari
## Date: Monday, January 16, 2023
## Description: This is a melting snowman game that allows for the
##  the user to click a category then try to guess the unknown words
##  with the clue present. Should the user click the wrong alphabet
##  buttons, then the snowman begins to melt. Once the snowman melts,
##  the game is over and the user lost. However, should the user
##  guess the unknown word before the snowman melts, then they will
##  win the game and have the option to restart the game and even
##  chose a different category to play with.
## Input: User inputs the category of the questions and input letters
##  in order to try to solve the unknown word with the clue they received.
############################################################################

# Imports pygame in order for the game to be played.
# Import random processes a random question every time a new game is played.
# Import time allows for time to be processed allowing for the game to run better.
# Output: Initializes pygame in order for it to pop up on the window.
import pygame
import random
import time
pygame.init()
 
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#

# Initializes the values and variables for each colour.
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED   = (255,0, 0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
LIGHT_BLUE = (102,255,255)

# Initializes the variables such as font, sound, clock, and text.
btn_font = pygame.font.SysFont("arial", 20)
titleFont = pygame.font.SysFont("arial", 60)
guess_font = pygame.font.SysFont("monospace", 24)
restart_font = pygame.font.SysFont("calibri", 13)
gameOver_font = pygame.font.SysFont("arial", 60)
clue_font = pygame.font.SysFont("monospace", 15)
correct = pygame.mixer.Sound('correct.ogg')
wrong = pygame.mixer.Sound('wrong.ogg')
winner = pygame.mixer.Sound('winner.ogg')
loser = pygame.mixer.Sound('loser.ogg')
clock = pygame.time.Clock()
title = titleFont.render('MELTING SNOWMAN', True, BLACK)

#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#

# Defines a createButtons function that allows for 26 buttons to be created.
# Process: This function intializes the coordinates and places for the buttons
#   to be placed and for 26 (a-z) to be produced in order for the user to be
#   able to guess the clues given the letters available to them. It then prints
#   and returns the buttons after the loop is completed.
def createButtons():
    x = 98
    y = 400
    buttons = []
    for btn in range(26):
        buttons.append((x,y))
        x += 42
        if btn == 12:
            x = 98
            y += 42
    print(buttons)
    return buttons

# Defines a drawButtons(buttons) functions that draws the buttons onto the game
#   window by being the colour light blue and having a white outline.
# Process: This function processes buttons to be drawn and by using mousePos,
#   it is able to identify that when a button is pressed, ti will change the colour
#   of that button so it camouflages with the background so the user knows which
#   button was previously pressed when playing the game.
def drawButtons(buttons):
    mousePos = pygame.mouse.get_pos()
    for i,xy in enumerate(buttons):
        ltrToRender = chr(i+65)
        a = mousePos[0] - xy[0]
        b = mousePos[1] - xy[1]
        c = (a**2 + b**2)**.5
        if c <= 15:
            colour = LIGHT_BLUE
        else:
            colour = WHITE
            if ltrToRender in usedLtrs:
                colour = LIGHT_BLUE
            else:
                colour = WHITE
        #circle(Surface, color, pos, radius, width=0) -> Rect
        pygame.draw.circle(win,colour,xy,18,0)
        pygame.draw.circle(win,BLACK,xy,18,4)
        #render(text, antialias, color, background=None) -> Surface
        ltrSurface = btn_font.render(ltrToRender,True,BLACK)
        win.blit(ltrSurface,(xy[0]-ltrSurface.get_width()//2,xy[1]-ltrSurface.get_height()//2))

# Process: Checks if a button has been clicked.
def clickBtn(mp,buttons):
    for i,xy in enumerate(buttons):
        a = mp[0] - xy[0]
        b = mp[1] - xy[1]
        c = (a**2 + b**2)**.5
        if c <= 15:
            usedLtrs.append(i)
            return i
    return -1

# Process: Loads the nine images of the snowman and stores them into a list.
def loadSnowmanImages():
    smImages = []
    for imgNum in range(9):
        fileName = 'snowman' + str(imgNum) + '.png'
        smImages.append(pygame.image.load(fileName))
    return smImages

# Process: Loads the puzzles that are created in the given text file.
def loadPuzzles():
    puzzles = [[],[],[]]
    fi = open('puzzle.txt','r')
    for p in fi:
        puz = p.strip().split(',')
        catIndex = int(puz[0])-1
        puzzles[catIndex].append(puz[1:])
    fi.close()
    return puzzles

# Process: Choses a random puzzle from the loaded puzzles and ensures it is not picked twice.
def getRandomPuzzle(cat, puzzles):
    pIndex = random.randrange(0, len(puzzles[cat]))
    while True:
        if pIndex in chosen:
            pIndex = random.randrange(0, len(puzzles[cat]))
        else:
            break
    chosen.append(pIndex)

    randomPuzz = puzzles[cat][pIndex]
    return randomPuzz

# Process: Creates a starting guess in which replaces all the letters that are hidden with underscores.
def initializeGuess(puzzle):
    guess = ''
    for c in puzzle:
        if c == ' ':
            guess += ' '
        else:
            guess += '_'
    return guess

# Process: Spaces out the underscores of the guess with spaces so the user knows the amount of letters present in the word.
def spacedOut(s):
    spaced_s = ''
    for c in s:
        spaced_s += c + ' '
    return spaced_s[:-1]

# Process: Draws the starting guess on the screen and gives the clue to the user.
def drawGuess():
    guessSurface = guess_font.render(spacedOut(guess),True,BLACK)
    x = (win.get_width() - guessSurface.get_width())//2
    win.blit(guessSurface,(x,280))
    clueSurface = clue_font.render(clue,True,BLACK)
    x = (win.get_width() - clueSurface.get_width())//2
    win.blit(clueSurface,(x,320))

# Process: Updates the guess with letters depending on the buttons clicked, and changes the underscores with the letters in the hidden word.
def updateGuess(ltrGuess,guess,puzzle):
    newGuess = ''
    for i,ltr in enumerate(puzzle):
        if ltrGuess == ltr:
            newGuess += ltr
        else:
            newGuess += guess[i]
    print(newGuess)
    return newGuess

# Process: Draws the category buttons and changes its colour if they are moused over.
def drawCatagoryButtons(catButtons):
    catMousePos = pygame.mouse.get_pos()
    for b in catButtons:
        if pygame.Rect(b[0]).collidepoint(catMousePos):
            catBtncolour = RED
        else:
            catBtncolour = BLACK
        pygame.draw.rect(win,catBtncolour,b[0],0)
        pygame.draw.rect(win,WHITE,b[0],3)
        txtSurface = btn_font.render(b[1],True,WHITE)
        x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
        y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
        win.blit(txtSurface,(x,y))

# Process: Checks to see if a category button has been clicked by the user.
def catBtnClick(mp,buttons):
    for i,b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            return i
    return -1

#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#

# Process: Redraws the game window depending on the screen it is category, game, game over), and animates the snowman
#   on the game screen correcty after wins, losses, and wrong guesses, and even updates the display.
def redraw_game_window():
    # code to draw things goes here
    if currentScreen == 1:
        win.fill(LIGHT_BLUE)
        win.blit(title, (52,30))
        win.blit(meltingSnowmanImage, (60,145))
        drawCatagoryButtons(catButtons)

    elif currentScreen == 2:
        win.fill(LIGHT_BLUE)
        drawButtons(buttons)
        win.blit(smImages[wrongCount], (175, 15))
        drawGuess()

        if wrongCount == 8:
            win.blit(lostSurface, (30,8))
            win.blit(lostSurface, (560,8))
            win.blit(playAgain, (10, 100))
            win.blit(quitGame, (10, 140))
            win.blit(changeCategory, (10, 175))
            win.blit(playAgain, (535, 100))
            win.blit(quitGame, (535, 140))
            win.blit(changeCategory, (535, 175))

        elif puzzle == guess:
            win.blit(wonSurface, (30,8))
            win.blit(playAgain, (10, 100))
            win.blit(quitGame, (10, 140))
            win.blit(changeCategory, (10, 175))
            win.blit(playAgain, (535, 100))
            win.blit(quitGame, (535, 140))
            win.blit(changeCategory, (535, 175))

    elif currentScreen == 3:
        win.fill(LIGHT_BLUE)
        win.blit(gameOver, (150, 80))
        win.blit(quitGame, (250, 200))
        win.blit(changeCategory, (250, 180))
        
    pygame.display.update()

#-------------------------------------#
# the main program begins here          #
#---------------------------------------#

# Initializes texts that need to be renderd and the category buttons with the category name given.
win = pygame.display.set_mode((700,480))
playAgain = restart_font.render('PLAY AGAIN? (Click a)', True, BLACK)
quitGame = restart_font.render('QUIT? (Click ESC)', True, BLACK)
changeCategory = restart_font.render('Change Category? (Click c)', True, BLACK)
gameOver = gameOver_font.render('GAME OVER!', True, BLACK)

catButtons = [[(56,130,160,80),'Famous Movies'],
              [(271,130,160,80),'Famous Athletes'],
              [(486,130,160,80),'Soccer Teams']]

wonSurface = guess_font.render("YOU WIN!",True,BLUE)
lostSurface = guess_font.render("YOU LOST!",True,RED)

awesomeImage = pygame.image.load('awesome.png')
meltingSnowmanImage = pygame.image.load('meltingsnowman.png')


# Intializes the variables to determine which screens are to be displayed and to set wrongCount to zero and current screen to one.
wrongCount = 0
currentScreen = 1
usedLtrs = []
chosen = []

inPlay = True

while inPlay:

    redraw_game_window()                           # window must be constantly redrawn - animation
    clock.tick(30)                          
    pygame.time.delay(10)                          # pause for 10 miliseconds
    
    for event in pygame.event.get():               # check for any events
        if event.type == pygame.QUIT:              # if user clicks on the window's 'X' button
            inPlay = False                         # exit from the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:       # if user clicks on the 'ESC' button
                inPlay = False                     # exit from the game
            if event.key == pygame.K_a:            # if user clicks on 'a' button
                buttons = createButtons()          # the game restarts in the same category
                smImages = loadSnowmanImages()
                puzzles = loadPuzzles()
                randomPuzz = getRandomPuzzle(cat, puzzles)
                puzzle = randomPuzz[0]
                clue = randomPuzz[1]
                print (puzzle)
                print (clue)
                guess = initializeGuess(puzzle)
                usedLtrs = []
                wrongCount = 0
                
            if event.key == pygame.K_c:            # if user clicks on the 'm' button
                chosen.clear()
                currentScreen = 1                  # they go back to the main menu (categories)
        if event.type == pygame.MOUSEBUTTONDOWN:   # if user clicks anywhere on win
            clickPos = pygame.mouse.get_pos()      # it knowns the mouse position on the screen in which it clicked

            if currentScreen == 1:                      # if they are on the main menu screen
                cat = catBtnClick(clickPos,catButtons)  # ensures and determines whihc category the user clicked
                if cat != -1:
                    currentScreen = 2                   # goes to the game screen when it becomes looped again
                    buttons = createButtons()           # ensures the game starts up
                    smImages = loadSnowmanImages()
                    puzzles = loadPuzzles()
                    randomPuzz = getRandomPuzzle(cat, puzzles)
                    puzzle = randomPuzz[0]
                    clue = randomPuzz[1]
                    print (puzzle)
                    print (clue)
                    guess = initializeGuess(puzzle)
                    usedLtrs = []
                    wrongCount = 0
                    
            elif currentScreen == 2:                                  # if they they are on the game screen
                if clickBtn(clickPos, buttons) != -1:
                    ltrGuess = chr(clickBtn(clickPos, buttons) + 65)  # figures out what button was clicked
                    print('You clicked on button: ', ltrGuess)        # prints the letter clicked
                    usedLtrs.append(ltrGuess)                         # adds the letter to a list
                    
                    if ltrGuess in puzzle:                            # if the letter is correct
                        correct.play()                                # correct guess sound is played
                        guess = updateGuess(ltrGuess,guess,puzzle)    # guess is updated
                        win.blit(awesomeImage, (10, 8))               # animation of the image becomes present
                        pygame.display.update()
                        pygame.time.wait(400)
            
                    else:                                             # if the letter is not correct
                        wrong.play()                                  # wrong guess sound is played
                        wrongCount += 1                               # adds another to wrong guess
                            
                    if wrongCount == 8:                               # if eight wrong guesses are made, the user loses
                        loser.play()                                  # game lost sound is played
                        if len(chosen) == 6:
                            pygame.time.wait(300)             
                            currentScreen = 3                         # screen changes to game over screen
                        
                    elif puzzle == guess:                             # if the user guesses the word, they win the game
                        winner.play()                                 # winner sound is played
                        if len(chosen) == 6:                          # the game finishes when the user runs out of puzzles
                            pygame.time.wait(300)
                            currentScreen = 3                         # screen changes to game over screen
                       
                                                           
pygame.quit()                                                         # quits pygame
