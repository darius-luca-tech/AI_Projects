import tkinter as tk
import mediahandler
#import chessgame
import bitboards as bb
import const

class GameDisplay( tk.Canvas ):
    
    def __init__(self, parent, manager):
        tmp_width = const.DEFAULTBORDERWIDTH*2 + const.DEFAULTTILEWIDTH*8
        tk.Canvas.__init__( self, parent, bg= const.COLORS["bg"], 
                            width= tmp_width, height= tmp_width )
        
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.dispScale = 1.0
        
        self.game = None        #will be assigned at manager init
        self.manager = manager
        
        self.mediaHandler = mediahandler.MediaHandler()
        self.loadImages()
        self.mediaHandler.setSize("tile", const.DEFAULTTILEWIDTH, const.DEFAULTTILEWIDTH)
        
        self.createChessboard()

        self.bind("<Button-1>", self.event_click)
        self.bind("<Configure>", self.event_resize)
        
        
    def event_click(self, event):
        #translating the event-coordinates to coordinates of the tile grid with (0,0) on top left        
        x = ( event.x/self.dispScale - const.DEFAULTBORDERWIDTH ) // const.DEFAULTTILEWIDTH 
        y = ( event.y/self.dispScale - const.DEFAULTBORDERWIDTH ) // const.DEFAULTTILEWIDTH 
        
        if( x in range(8) and y in range(8) ):
            self.manager.event_chessboardClick( int( x +(7- y) * 8 ) )      #sq = x + (7-y)*8
        
        
    def event_resize(self, event):
        scale = float( min( event.height, event.width ) ) / min( self.width, self.height )
        
        self.width = event.width
        self.height = event.height
        
        self.scale(tk.ALL, 0, 0, scale, scale)
        
        self.dispScale *= scale
        
        self.delete("image")
        self.createChessmen()
        self.createBoardCommentary()
        
        
    def getTilePos(self, sq):
        return (    self.dispScale * ( const.DEFAULTBORDERWIDTH+const.DEFAULTTILEWIDTH*(bb.line(sq)) ), \
                    self.dispScale * ( const.DEFAULTBORDERWIDTH+const.DEFAULTTILEWIDTH*(7-bb.rank(sq)) )    )
    
    
    def addVec(self, p1, p2):
        return (p1[0]+p2[0], p1[1]+p2[1])
        
        
    def loadImages(self):
        #chessmen
        for color in (const.WHITE, const.BLACK):
            for name in const.FIGURE_NAME[1::]:
                name += str(color)
                self.mediaHandler.loadImage( name, "tile", "./media/chessmen/%s.png" % name )
        
        #highlight tiles
        for x in range(4):
            self.mediaHandler.loadImage("highlight%i" % x, "tile", "./media/highlight%i.png" % x )
        
        #bord font
        for n in range(1, 9):
            self.mediaHandler.loadImage(str(n), "font", "./media/font/%i.png" % n )
            self.mediaHandler.loadImage(chr(96+n), "font", "./media/font/%s.png" % chr(96+n) )
            
            
    def update(self):
        self.delete("chessman")
        self.createChessmen()
        
            
    def removeHighlight(self):
        self.delete("highlight")        
        
            
    def highlightTile(self, sq, n):
        #for sq in moves:
        self.create_image(  self.getTilePos(sq),
                            image= self.mediaHandler.imagesTk["tile"]["highlight%i" % n],
                            anchor= tk.NW,
                            tags= ("highlight", "image") )
    
    
    def createChessboard(self):
        edgeLength= min( self.height, self.width )
        
        #border
        self.create_rectangle( 0, 0,
                               edgeLength, edgeLength,
                               fill= const.COLORS["border"] )
        
        #tiles
        for sq in range(64):
            self.create_rectangle(  self.getTilePos( sq ),
                                    self.addVec( self.getTilePos( sq ), (self.dispScale*const.DEFAULTTILEWIDTH, self.dispScale*const.DEFAULTTILEWIDTH)),
                                    fill= const.COLORS["tiles"][ (sq+bb.rank(sq))%2 ] ) 
        
    
    def createBoardCommentary(self):       
        self.mediaHandler.setSize( "font", self.dispScale*const.DEFAULTFONTSIZE[0], self.dispScale*const.DEFAULTFONTSIZE[1] )
        
        for x in range(8):
            self.create_image( self.addVec(self.getTilePos(56-x*8), (-const.DEFAULTBORDERWIDTH*self.dispScale/2, const.DEFAULTTILEWIDTH*self.dispScale/2) ),
                               image= self.mediaHandler.imagesTk["font"][str(8-x)],
                               anchor= tk.CENTER,
                               tags= ("font", "image") )
            self.create_image( self.addVec(self.getTilePos(56+x), (const.DEFAULTTILEWIDTH*self.dispScale/2, -const.DEFAULTBORDERWIDTH*self.dispScale/2 ) ),
                               image= self.mediaHandler.imagesTk["font"][chr(x+97)],
                               anchor= tk.CENTER,
                               tags= ("font", "image") )
            
            
    def createChessmen(self):
        if( not self.game ):
            return
        
        self.mediaHandler.setSize( "tile", self.dispScale*const.DEFAULTTILEWIDTH, self.dispScale*const.DEFAULTTILEWIDTH )
        
        for sq in range(64):
            figure = abs(self.game.board[sq])
            color = const.WHITE if self.game.board[sq] > 0 else const.BLACK
            
            if(figure != 0):
                self.create_image(  self.getTilePos(sq),
                                    image= self.mediaHandler.imagesTk["tile"][const.FIGURE_NAME[figure]+str(color)],
                                    anchor= tk.NW,
                                    tags= ("chessman", "image") )
                
                
                
                
                