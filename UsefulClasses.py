import pygame

# This class can be used to make a call back function that runs at any time interval
# Perfect for game time, etc.  Just set the "timeBetweenCallbacks" to 1 for a 1 second timer!
from threading import Timer,Thread,Event
class perpetualTimer():

   def __init__(self,timeBetweenCallbacks,hFunction):
      self.timeBetweenCallbacks=timeBetweenCallbacks
      self.hFunction = hFunction
      self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)
      self.running = True

   def Stop(self):
      self.running = False

   def handle_function(self):
      self.hFunction()
      #The timer carrys on each time because it makes a new one each time in the handling function.
      #Stop the timer just don't make the new timer!!!
      if(self.running == True):
        self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)
        self.thread.daemon = True 
        self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

#Like the class above, but will only call the callback function one time before the thread dies.
class DelayedFunctionCall():

   def __init__(self,timeBetweenCallbacks,hFunction):
      self.timeBetweenCallbacks=timeBetweenCallbacks
      self.hFunction = hFunction
      self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)

   def handle_function(self):
      self.hFunction()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

#Clickable image button class with callback function

class MyClickableImageButton:
    def __init__(self, x, y, newImage,newGreyImg,newParentSurface,theNewCallback):
        self.img=newImage
        self.greyImg = newGreyImg
        self.rect=self.img.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
        self.parentSurface=newParentSurface
        self.theCallback = theNewCallback

    def DrawSelf(self):
        #The button will be grey until the mouse hovers over it!
        self.parentSurface.blit(self.greyImg, (self.rect.x, self.rect.y))
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked=True
                self.theCallback()
            if not pygame.mouse.get_pressed()[0]:
                self.clicked=False
                self.parentSurface.blit(self.img, (self.rect.x, self.rect.y))

class Piece(pygame.sprite.Sprite): 
    def __init__(self, newImage, newParentSurface, newPlayerNum,newBeingDragged): 
        super().__init__() 

        self._image = newImage
        self._parentSurface = newParentSurface
        self._playerNum = newPlayerNum
        self._beingDragged = newBeingDragged

    def DrawSelf(self,somePos):
        self._parentSurface.blit(self._image, somePos)

    def SetDragged(self, newBeingDragged):
        self._beingDragged = newBeingDragged

    def GetDragged(self):
        return self._beingDragged

    def GetPlayerNum(self):
        return self._playerNum
    
    def SetImage(self, newImage):
        self._image = newImage

    def GetImage(self):
        return self._image

#A Generic game grid class - It deals with the dreaded "rows" and "cols" V (x,y) situation for easy coding!
class MyGameGrid():
    
    def __init__(self,newRows,newCols,newCellSizeX,newCellSizeY,newTopLeftPos,newPieceOffsetX,newPieceOffsetY,newGridLinesCol):
        self._rows = newRows
        self._cols = newCols
        self._cellSizeX = newCellSizeX
        self._cellSizeY = newCellSizeY
        self._topLeftPos = newTopLeftPos
        self._pieceOffsetX = newPieceOffsetX
        self._pieceOffsetY = newPieceOffsetY
        self._gridLinesCol = newGridLinesCol
        self._pieceBeingDragged = None
        self._theGrid = list()
        self.BlankTheGrid()
        
    def BlankTheGrid(self):
        #Make the whole grid "blank"
        self._theGrid = list()
        for i in range(self._rows):
            newRow = []
            for j in range(self._cols):
                newRow.append(None)
        
            self._theGrid.append(newRow)

    def GetGridItem(self,theCoord):
        #The x and y are coords starting at zero of a position on the game grid that we want
        #
        #  -------------------------
        #  | 0,0 | 1,0 | 2,0 | 3,0 |
        #  -------------------------
        #  | 0,1 | 1,1 | 2,1 | 3,1 |
        #  -------------------------
        #  | 0,2 | 1,2 | 2,2 | 3,2 |
        #  -------------------------
        #
        #  etc.

        #The problem is that the game grid is stored in a list of lists(rows), so:
        #
        # x is col!
        # y is the row!
        #
        # We need to access items using theGrid[y][x]

        x = theCoord[0]
        y = theCoord[1]
        return self._theGrid[y][x]

    def SetGridItem(self,theCoord,newItem):
        x = theCoord[0]
        y = theCoord[1]
        self._theGrid[y][x] = newItem 

    def DrawSelf(self):

        rowNum = 0
        for row in self._theGrid:
            colNum = 0
            for somePiece in row:
                if(somePiece != None):
                    thePos = (self._topLeftPos[0] + colNum*self._cellSizeX + self._pieceOffsetX,
                              self._topLeftPos[1] + rowNum*self._cellSizeY + self._pieceOffsetY)
                    somePiece.DrawSelf(thePos)
                colNum = colNum + 1
            rowNum = rowNum + 1

    def DebugPrintSelf(self):
        for row in self._theGrid:
            for somePiece in row:
                if(somePiece == None):
                    print(0,end=" ")
                else:
                    print(somePiece.GetPlayerNum(),end=" ")
            print("")
        
        print("Dragged piece : " + str(self._pieceBeingDragged))
    
    def DrawGridLines(self,someSurface): 
        LINE_WIDTH = 3
        for i in range(self._cols + 1):
            pygame.draw.line(someSurface,self._gridLinesCol,(self._topLeftPos[0]+i*self._cellSizeX, self._topLeftPos[1]),
                                                            (self._topLeftPos[0]+i*self._cellSizeX, self._topLeftPos[1] + (self._rows)*self._cellSizeY),LINE_WIDTH)
        for i in range(self._rows + 1):
            pygame.draw.line(someSurface,self._gridLinesCol,(self._topLeftPos[0], self._topLeftPos[1]+i*self._cellSizeY),
                                                            (self._topLeftPos[0]+(self._cols)*self._cellSizeX, self._topLeftPos[1]+i*self._cellSizeY),LINE_WIDTH)

    def WhatSquareAreWeIn(self,someMousePosition):
        #Find out what square somebody clicked on.
        #For example, if we click top left the the answer is row 0 col 0
        currentClickX = someMousePosition[0]
        currentClickY = someMousePosition[1]
    
        adjustedX = currentClickX-self._topLeftPos[0]
        col = adjustedX//(self._cellSizeX)
        #col = adjustedX//(self._cellSizeX+1) #The +1 in the brackets seems to fix the identifcation of col 6 to 7 which was a bit out?
    
        adjustedY = currentClickY-self._topLeftPos[1]
        row = adjustedY//(self._cellSizeY)
    
        return col,row
                    
            