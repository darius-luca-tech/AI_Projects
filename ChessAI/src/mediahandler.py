from PIL import Image, ImageTk
import PIL

class MediaHandler():
    def __init__(self):
        self.imagesRaw = { }
        self.imagesTk = { }
        
    def loadImage(self, name, tag, path):
        if( not tag in self.imagesRaw ):
            self.imagesRaw[tag] = { }
            self.imagesTk[tag] = { }
        
        self.imagesRaw[tag][name] = Image.open(path)
        self.imagesTk[tag][name] = PIL.ImageTk.PhotoImage( self.imagesRaw[tag][name] )
        
    def setSize(self, tag, width, height ):
        width, height = int(width), int(height)
        
        for key in self.imagesRaw[tag].keys():
            new_image = self.imagesRaw[tag][key].resize( (width, height), PIL.Image.ANTIALIAS)
            self.imagesTk[tag][key] = PIL.ImageTk.PhotoImage( new_image )
            
        
