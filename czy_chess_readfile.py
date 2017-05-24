###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################

#imports
import Rhino as r
import rhinoscriptsyntax as rs

from Rhino.FileIO import FileReadOptions
import scriptcontext as sc

import czy_chess_fileinfo as fin

#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2



class read:
    def __init__(self,filepaths):
        opt=FileReadOptions()
        opt.ImportMode=True
        for f in filepaths:
            sc.doc.ReadFile(f,opt)
            
    def all(self):
        objtype=r.DocObjects.ObjectType.AnyObject
        objs=sc.doc.Objects.GetObjectList(objtype)
        return objs
        
    def bylayer(self,layer):
        objs=sc.doc.Objects.FindByLayer(layer)
        
        return objs
        
    def curves(self):
        objtype=r.DocObjects.ObjectType.Curve
        crvs=sc.doc.Objects.GetObjectList(objtype)
        return crvs
    
    def delete(self):
        for obj in self.objs:
            rs.DeleteObject(obj)
        return OK

"""def main():
    
    fpath=fin.filepath()
    pawnfile=fpath.pawn()
    knightfile=fpath.knight()
    bishopfile=fpath.bishop()
    queenfile=fpath.queen()
    kingfile=fpath.king()
    rookfile=fpath.rook()
    
    rd=read(pawnfile)
    
    return OK
    
main()"""