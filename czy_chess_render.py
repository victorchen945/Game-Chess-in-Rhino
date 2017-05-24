###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules 
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino as r
from czy_chess_fileinfo import filepath
from czy_chess_readfile import read 


#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2


BLACK=(0,0,0)
WHITE=(255,255,255)
menblack=(80,80,80)
menwhite=(200,200,200)
RED=(255,0,0)
YELLOW=(255,255,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
NONE=None
SCALE=10
    
class chesstable:
        
    def render(self,objs,color):
        for obj in objs:
            #get object material index
            index=rs.ObjectMaterialIndex(obj)
            #render color(material)
            if index==-1:
                index=rs.AddMaterialToObject(obj)
                rs.MaterialColor(index,color)
            #display color
            rs.ObjectColor(obj,color)
        return OK
        
    def table(self,table):
        for i in range(8):
            for j in range(8):
                rec=rs.AddRectangle((i*SCALE,j*SCALE,0),SCALE,SCALE)
                srf=rs.AddPlanarSrf(rec)
                if table[i][j].baseclr=="BLACK":
                    self.render(srf,BLACK)
                elif table[i][j].baseclr=="WHITE":
                    self.render(srf,WHITE)
                else:
                    print "error in drawing"
                    return ERROR
                table[i][j].cell=srf
                
        return OK
        

class boxcolor:
    
    def red(self,box):
        index=rs.ObjectMaterialIndex(box.cell)
        if index==-1:
            index=rs.AddMaterialToObject(box.cell)
        rs.MaterialColor(index,RED)
        return OK
        
    def yellow(self,box):
        index=rs.ObjectMaterialIndex(box.cell)
        if index==-1:
            index=rs.AddMaterialToObject(box.cell)
        rs.MaterialColor(index,YELLOW)
        return OK
    
    def green(self,box):
        index=rs.ObjectMaterialIndex(box.cell)
        if index==-1:
            index=rs.AddMaterialToObject(box.cell)
        rs.MaterialColor(index,GREEN)
        
    def blue(self,box):
        index=rs.ObjectMaterialIndex(box.cell)
        if index==-1:
            index=rs.AddMaterialToObject(box.cell)
        rs.MaterialColor(index,BLUE)
        
    def default(self,box):
        index=rs.ObjectMaterialIndex(box.cell)
        
        if index==-1:
            index=rs.AddMaterialToObject(box.cell)
        print index
        print box.baseclr
        if box.baseclr is None:
            print ERROR
        if box.baseclr=="BLACK":
            rs.MaterialColor(index,BLACK)
        elif box.baseclr=="WHITE":
            rs.MaterialColor(index,WHITE)
        return OK

class chessmen:
    def __init__(self):
        self.fpaths=filepath()
        self.renderbox=chesstable()
        
    
    def simple(self,box):
        #for test play
        ptoffset=(-SCALE/2,-SCALE/2,0)
        if box.type=="P":
            box.chessmen=rs.AddText("P",rs.PointAdd(box.cen,ptoffset),SCALE)
            rs.LockObjects(box.chessmen)
        if box.type=="R":
            box.chessmen=rs.AddText("R",rs.PointAdd(box.cen,ptoffset),SCALE)
            rs.LockObjects(box.chessmen)
        if box.type=="N":
            box.chessmen=rs.AddText("N",rs.PointAdd(box.cen,ptoffset),SCALE)
            rs.LockObjects(box.chessmen)
        if box.type=="B":
            box.chessmen=rs.AddText("B",rs.PointAdd(box.cen,ptoffset),SCALE)
            rs.LockObjects(box.chessmen)
        if box.type=="Q":
            box.chessmen=rs.AddText("Q",rs.PointAdd(box.cen,ptoffset),SCALE)
            rs.LockObjects(box.chessmen)
        if box.type=="K":
            box.chessmen=rs.AddText("K",rs.PointAdd(box.cen,ptoffset),SCALE)
            rs.LockObjects(box.chessmen)
            
        if not (box.chessmen is None):
            if box.menclr=="BLACK":
                rs.ObjectColor(box.chessmen,[70,70,70])
            else:
                rs.ObjectColor(box.chessmen,[200,200,200])
        
        return box.chessmen
    
        
        
    def volumn(self,box):
        ptoffset=(-SCALE/2,-SCALE/2,0)
        if box.type=="P":
            rd=read(self.fpaths.pawn())
            pawn=rd.bylayer("pawn")
            xform=rs.VectorCreate(box.cen,[0,0,0])
            newpawn=rs.MoveObjects(pawn,xform)
            for obj in newpawn:
                rs.ObjectLayer(obj,"chessmen")
            ##rs.LockObjects(pawn)
            if box.menclr=="WHITE":
                self.renderbox.render(newpawn,menwhite)
            elif box.menclr=="BLACK":
                self.renderbox.render(newpawn,menblack)
            box.chessmen=newpawn
            rs.LockObjects(box.chessmen)
            return pawn
        if box.type=="R":
            rd=read(self.fpaths.rook())
            rook=rd.bylayer("rook")
            xform=rs.VectorCreate(box.cen,[0,0,0])
            newrook=rs.MoveObjects(rook,xform)
            for obj in newrook:
                rs.ObjectLayer(obj,"chessmen")
            ##rs.LockObjects(rook)
            if box.menclr=="WHITE":
                self.renderbox.render(newrook,menwhite)
            elif box.menclr=="BLACK":
                self.renderbox.render(newrook,menblack)
            box.chessmen=newrook
            rs.LockObjects(box.chessmen)
            return rook
        if box.type=="N":
            rd=read(self.fpaths.knight())
            knight=rd.bylayer("knight")
            xform=rs.VectorCreate(box.cen,[0,0,0])
            newknight=rs.MoveObjects(knight,xform)
            for obj in newknight:
                rs.ObjectLayer(obj,"chessmen")
            if box.menclr=="WHITE":
                self.renderbox.render(newknight,menwhite)
            elif box.menclr=="BLACK":
                self.renderbox.render(newknight,menblack)
            box.chessmen=newknight
            rs.LockObjects(box.chessmen)
            return knight
        if box.type=="B":
            rd=read(self.fpaths.bishop())
            bishop=rd.bylayer("bishop")
            xform=rs.VectorCreate(box.cen,[0,0,0])
            newbishop=rs.MoveObjects(bishop,xform)
            for obj in newbishop:
                rs.ObjectLayer(obj,"chessmen")
            if box.menclr=="WHITE":
                self.renderbox.render(newbishop,menwhite)
            elif box.menclr=="BLACK":
                self.renderbox.render(newbishop,menblack)
            box.chessmen=newbishop
            rs.LockObjects(box.chessmen)
            return bishop
        if box.type=="K":
            rd=read(self.fpaths.king())
            king=rd.bylayer("king")
            xform=rs.VectorCreate(box.cen,[0,0,0])
            newking=rs.MoveObjects(king,xform)
            for obj in newking:
                rs.ObjectLayer(obj,"chessmen")
            if box.menclr=="WHITE":
                self.renderbox.render(newking,menwhite)
            elif box.menclr=="BLACK":
                self.renderbox.render(newking,menblack)
            box.chessmen=newking
            rs.LockObjects(box.chessmen)
            return king
        if box.type=="Q":
            rd=read(self.fpaths.queen())
            queen=rd.bylayer("queen")
            xform=rs.VectorCreate(box.cen,[0,0,0])
            newqueen=rs.MoveObjects(queen,xform)
            for obj in newqueen:
                rs.ObjectLayer(obj,"chessmen")
            if box.menclr=="WHITE":
                self.renderbox.render(newqueen,menwhite)
            elif box.menclr=="BLACK":
                self.renderbox.render(newqueen,menblack)
            box.chessmen=newqueen
            rs.LockObjects(box.chessmen)
            return queen
        return OK

"""def main():
    mymen=chessmen()
    objs=mymen.pawn()
    rs.LockObjects(objs)
    return OK

main()"""