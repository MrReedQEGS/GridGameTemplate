# This class can be used to make a call back function that runs at any time interval
# Perfect for game time, etc.  Just set the "timeBetweenCallbacks" to 1 for a 1 second timer!
from threading import Timer,Thread,Event
class perpetualTimer():

   def __init__(self,timeBetweenCallbacks,hFunction):
      self.timeBetweenCallbacks=timeBetweenCallbacks
      self.hFunction = hFunction
      self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.timeBetweenCallbacks,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

#Clickable image button class with callback function
import pygame
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


#A Generic game grid class - It deals with the dreaded "rows" and "cols" V (x,y) situation for easy coding!
class MyGameGrid():
    def __init__(self,newRows,newCols,newListOfAllowedCellItems,newPosOfBlankItem):
        self.rows = newRows
        self.cols = newCols
        self.listOfAllowedCellItems = newListOfAllowedCellItems
        self.posOfBlankItem = newPosOfBlankItem  #The position in the allowed items list of the thing that represents "BLANK"
        self.BlankTheGrid()

    def BlankTheGrid(self):
        #Make the whole grid "blank"
        blankThing = self.listOfAllowedCellItems[self.posOfBlankItem]
        self.theGrid = list()
        for i in range(self.rows):
            newRow = []
            for j in range(self.cols):
                newRow.append(blankThing)
        
            self.theGrid.append(newRow)

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
        return self.theGrid[y][x]

    def SetGridItem(self,theCoord,newItem):
        x = theCoord[0]
        y = theCoord[1]
        self.theGrid[y][x] = newItem 

    def DebugPrintSelf(self):
        for row in self.theGrid:
            print(row)