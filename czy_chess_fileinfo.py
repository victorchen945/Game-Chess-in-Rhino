###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules 
import rhinoscriptsyntax as rs
import scriptcontext as sc

#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2


class filepath:
    def __init__(self):
        self.filepath="C:\Users\Administrator\Desktop\wheels\chess\chessmen"
        #self.filepath="C:\Users\Administrator\Desktop\WHEELFAC\GAME\chess\chessmen"
        
    def pawn(self):
        pawn=self.filepath+"\pawn1.3dm"
        return [pawn]
    
    def knight(self):
        knight=self.filepath+"\knight.3dm"
        return [knight]
    
    def bishop(self):
        bishop=self.filepath+"\Bishop.3dm"
        return [bishop]
    
    def rook(self):
        rook=self.filepath+"\Rook.3dm"
        return [rook]
        
    def king(self):
        king=self.filepath+"\king.3dm"
        return [king]
        
    def queen(self):
        queen=self.filepath+"\Queen.3dm"
        return [queen]

