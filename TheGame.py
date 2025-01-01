##############################################################################
# DETAILS
#  A good template for a grid game of some kind
#  Mr Reed - Dec 2024
#
#  Sounds 
#  https://pixabay.com/sound-effects/search/clicks/
#
#  Music
#  https://pixabay.com/music/search/relaxing%20game%20music/
#
#  Sprite sheet
#  https://www.finalparsec.com/tools/sprite_sheet_maker
#
#
##############################################################################

##############################################################################
# IMPORTS
##############################################################################
import pygame, random, time
from pygame.locals import *
from UsefulClasses import perpetualTimer,MyGameGrid,MyClickableImageButton,Piece

import tkinter
from tkinter import messagebox

##############################################################################
# VARIABLES
##############################################################################

APP_NAME = "Grid game temmplate"
COPYRIGHT_MESSAGE = "Mark Reed (c) 2024"
WINDOW_TEXT = APP_NAME + " - " + COPYRIGHT_MESSAGE

#CREATE THE EMPTY GAME GRID OBJECT
EMPTY_SQUARE = 0
PLAYER1 = 1
PLAYER2 = 2

GAMECOLS = 12
GAMEROWS = 8

GRID_SIZE_X = 52
GRID_SIZE_Y = 52
TOP_LEFT = (26,28)
PIECE_OFFSET_X = 4
PIECE_OFFSET_Y = 6

RIGHT_MOUSE_BUTTON = 3

DEBUG_ON = False

SCREEN_WIDTH = 678
SCREEN_HEIGHT = 504

BUTTON_X_VALUE = 526
BUTTON_Y_VALUE  = 472
BUTTON_WIDTH = 30

gridLinesOn = False

GAME_TIME_X = 2
GAME_TIME_Y = BUTTON_Y_VALUE + 5

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#surface.set_colorkey((255, 255, 255))  #White background sprites should now be transparent background!
pygame.display.set_caption(WINDOW_TEXT)

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREEN = (0,255,0)
BACK_FILL_COLOUR = COL_WHITE

backImageName = "./images/backgroundGrid.jpg"
undoImageName = "./images/Undo.jpg"
undoImageGreyName = "./images/UndoGrey.jpg"
muteImageName = "./images/Mute.jpg"
muteImageGreyName = "./images/MuteGrey.jpg"
infoImageName = "./images/Info.jpg"
infoImageGreyName = "./images/InfoGrey.jpg"
eyeImageName = "./images/Eye.jpg"
eyeImageGreyName = "./images/EyeGrey.jpg"
restartImageName = "./images/Restart.jpg"
restartImageGreyName = "./images/RestartGrey.jpg"

player1PieceImageName = "./images/player1Piece.png"
player2PieceImageName = "./images/player2Piece.png"

PIECE_SIZE = 20

#sounds
pygame.mixer.init()
clickSound = pygame.mixer.Sound("./sounds/click.mp3")
pygame.mixer.music.load("./sounds/relaxing-music.mp3") 

musicOn = False
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.pause()

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 16)

running = True

turn = COL_BLACK

#Timer callbacks
def OneSecondCallback():
    #Update game time
    global gameTime
    gameTime = gameTime + 1

gameTime = 0
gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
DELAY_1 = 1
myOneSecondTimer = None
if(myOneSecondTimer == None):
    myOneSecondTimer = perpetualTimer(DELAY_1,OneSecondCallback)
    myOneSecondTimer.start()

##############################################################################
# SUB PROGRAMS
##############################################################################
def TurnOffTimers():
        
    global myOneSecondTimer
    if(myOneSecondTimer!=None):
        myOneSecondTimer.Stop()
        myOneSecondTimer = None
        if(DEBUG_ON):
            print("Turnning off timer...myOneSecondTimer")

def LoadImages():
    global backImage,undoImage,undoGreyImage,muteImage,muteGreyImage
    global infoImage,infoGreyImage,player1PieceImage,player2PieceImage
    global eyeImage,eyeGreyImage,restartImage,restartGreyImage
 
    backImage = pygame.image.load(backImageName).convert()

    #Load an image with a white background and set the white to transparent.
    #Will only work if the background is all properly white 255,255,255
    player1PieceImage = pygame.image.load(player1PieceImageName)
    player1PieceImage = pygame.transform.scale(player1PieceImage, (43, 43))  #change size first before doing alpha things
    player1PieceImage.set_colorkey((255,255,255))
    player1PieceImage.convert_alpha()

    player2PieceImage = pygame.image.load(player2PieceImageName)
    player2PieceImage = pygame.transform.scale(player2PieceImage, (43, 43))  #change size first before doing alpha things
    player2PieceImage.set_colorkey((255,255,255))
    player2PieceImage.convert_alpha()
    
    undoImage = pygame.image.load(undoImageName).convert()
    undoGreyImage = pygame.image.load(undoImageGreyName).convert()
    muteImage = pygame.image.load(muteImageName).convert()
    muteGreyImage = pygame.image.load(muteImageGreyName).convert()
    infoImage = pygame.image.load(infoImageName).convert()
    infoGreyImage = pygame.image.load(infoImageGreyName).convert()
    eyeImage = pygame.image.load(eyeImageName).convert()
    eyeGreyImage = pygame.image.load(eyeImageGreyName).convert()
    restartImage = pygame.image.load(restartImageName).convert()
    restartGreyImage = pygame.image.load(restartImageGreyName).convert()

def HandleInput(running):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            currentMousePos = pygame.mouse.get_pos()
            currentSquare = theGameGrid.WhatSquareAreWeIn(currentMousePos)
            thingAtThatPosition = theGameGrid.GetGridItem(currentSquare)

            #print("Square clicked in : ", currentSquare)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_BUTTON:
                print ("You clicked the right mouse button")

            else:
                #did we click on a piece...if so we need to drag it around!
                if(thingAtThatPosition != None):
                    #player is picking up a piece - the clicked square is not empty!
                    thingAtThatPosition.SetDragged(True)
                    thingAtThatPosition.SetPickedUpFromLocation(currentSquare)
                    theGameGrid.SetDraggedPiece(thingAtThatPosition)
                    theGameGrid.SetGridItem(currentSquare,None)
            
            if(DEBUG_ON):
                theGameGrid.DebugPrintSelf()

        elif event.type == pygame.MOUSEBUTTONUP:
            #print("Mouse up")
            currentMousePos = pygame.mouse.get_pos()
            currentSquare = theGameGrid.WhatSquareAreWeIn(currentMousePos)
            thingAtThatPosition = theGameGrid.GetGridItem(currentSquare)

            someDraggedPiece = theGameGrid.GetDraggedPiece()
            if(someDraggedPiece != None):
                #we are dragging, so put it down...if the Square is empty
                theGameGrid.SetDraggedPiece(None)

                if(thingAtThatPosition == None and theGameGrid.OutsideGrid(currentSquare) == False):
                    theGameGrid.SetGridItem(currentSquare,someDraggedPiece)
                else:
                    #the piece cannot go here...put it back to the place it came from
                    whereItCameFrom = someDraggedPiece.GetPickedUpFromLocation()
                    theGameGrid.SetGridItem(whereItCameFrom,someDraggedPiece)

                someDraggedPiece.SetDragged(False)

            if(DEBUG_ON):
                theGameGrid.DebugPrintSelf()
           
    return running

def EyeButtonCallback():
    global gridLinesOn
    gridLinesOn = not gridLinesOn

def UndoButtonCallback():
    print("undo pressed...")

def RestartButtonCallback():

    #Use a TKINTER message box :)
    #Turn events off and then back on to stop pygame picking up the mouse click too!
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP) 
    answer = messagebox.askyesno("Question","Do you really to reset the whole game?")
    if(answer):
        PutPiecesInStartingPositions()
    pygame.event.set_allowed(None)

def MuteButtonCallback():
    global musicOn
    if(musicOn):
        musicOn = False
        pygame.mixer.music.pause()
    else:
        musicOn = True
        pygame.mixer.music.unpause()
            
def InfoButtonCallback():
   print("Info pressed")

def PutPiecesInStartingPositions():

    theGameGrid.BlankTheGrid()

    for i in range(8):
        someGamePiece = Piece(player1PieceImage,surface,PLAYER1,False)
        theGameGrid.SetGridItem((9,i),someGamePiece)
        
    for i in range(4):
        someGamePiece = Piece(player1PieceImage,surface,PLAYER1,False)
        theGameGrid.SetGridItem((10,i),someGamePiece)
        
    for i in range(4):
        someGamePiece = Piece(player2PieceImage,surface,PLAYER2,False)
        theGameGrid.SetGridItem((10,4+i),someGamePiece)
        
    for i in range(8):
        someGamePiece = Piece(player2PieceImage,surface,PLAYER2,False)
        theGameGrid.SetGridItem((11,i),someGamePiece)
        
##############################################################################
# MAIN
##############################################################################
pygame.init()

theGameGrid = MyGameGrid(GAMEROWS,GAMECOLS,GRID_SIZE_X,GRID_SIZE_Y,TOP_LEFT,PIECE_OFFSET_X,PIECE_OFFSET_Y,COL_GREEN)

LoadImages()

theRestartButton = MyClickableImageButton(BUTTON_X_VALUE,BUTTON_Y_VALUE,restartImage,restartGreyImage,surface,RestartButtonCallback)
theEyeButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*1,BUTTON_Y_VALUE,eyeImage,eyeGreyImage,surface,EyeButtonCallback)
theInfoButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*2,BUTTON_Y_VALUE,infoImage,infoGreyImage,surface,InfoButtonCallback)
theMuteButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*3,BUTTON_Y_VALUE,muteImage,muteGreyImage,surface,MuteButtonCallback)
theUndoButton = MyClickableImageButton(BUTTON_X_VALUE + BUTTON_WIDTH*4,BUTTON_Y_VALUE,undoImage,undoGreyImage,surface,UndoButtonCallback)

allPieces = []
PutPiecesInStartingPositions()

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (1, 1))

    if(gridLinesOn):
        theGameGrid.DrawGridLines(surface)

    theRestartButton.DrawSelf()
    theEyeButton.DrawSelf()
    theInfoButton.DrawSelf()
    theMuteButton.DrawSelf()
    theUndoButton.DrawSelf()

    running = HandleInput(running)
   
    #We may be dragging a particular piece!
    #TODO - Draw the dragged piece on the mouse if there is one.

    ##Draw all pieces that are on the board.
    currentMousePos = pygame.mouse.get_pos()
    theGameGrid.DrawSelf(currentMousePos)
       
    if(running):
        gameTimeSurface = my_font.render("Time elapsed : {}".format(gameTime), False, (0, 0, 0))
        surface.blit(gameTimeSurface, (GAME_TIME_X,GAME_TIME_Y))
        pygame.display.flip()

TurnOffTimers()

pygame.quit()