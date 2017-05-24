###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules 
import rhinoscriptsyntax as rs
import scriptcontext as sc


import czy_chesstable as tb
import czy_chess_render as dr

import czy_chessmen as chessmen


#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

def majesty(table,kingbox):
    #store the king location for each side
    color=kingbox.menclr
    if color==None:
        return ERROR
    for i in range(8):
        for j in range(8):
            if table[i][j].menclr==color and table[i][j].type!="K":
                table[i][j].ourking=kingbox
    return OK
    

def srfcompare(srf1,srf2):
    pt1=rs.SurfaceAreaCentroid(srf1)
    pt2=rs.SurfaceAreaCentroid(srf2)
    if rs.PointCompare(pt1[0],pt2[0])==TRUE:
        return TRUE
    else:
        return FALSE

def select(lastbox,table,step,record):
    #lastbox:last selected box, table:chesstable, step: current step
    #if last box exists, set last selection to defaut color
    mysel=dr.boxcolor()
    curstep=step
    moverecord=record
    #select box
    srf=rs.GetObject("select box",rs.filter.surface)
    #set color to default while change selection
    if not (lastbox is None):
        mysel.default(lastbox)
        if not (lastbox.next is None):
            for box in lastbox.next:
                mysel.default(box)
        if (lastbox.specialnext is not None) and len(lastbox.specialnext):
            if lastbox.type=="K":
                for box in lastbox.specialnext:
                    mysel.default(box[0])
            if lastbox.type=="P":
                for box in lastbox.specialnext:
                    mysel.default(box)
    for i in range(8):
        for j in range(8):
            if srfcompare(table[i][j].cell,srf)==TRUE:
                selsrf=table[i][j].cell
                if (not (table[i][j].type is None)) and stepmonitor(curstep,table[i][j])==TRUE :
                    mysel.green(table[i][j])
                    menmove=callmen(table,i,j,moverecord)
                else:
                    mysel.yellow(table[i][j])
                print "loc:",table[i][j].loc,"  type:",table[i][j].type,"  color:",table[i][j].menclr
                print "step:", curstep, table[i][j].menclr
                if table[i][j].ourking: print "  our king loc:", table[i][j].ourking.loc
                curbox=table[i][j]
    #move
    if not (lastbox is None):
        if not (lastbox.next is None) and len(lastbox.next):
            
            for mv in lastbox.next:
                if curbox.loc==mv.loc :
                    mymove=move(lastbox,curbox)
                    mymove.movemen()
                    curstep+=1
                    #if the king is moved ,renew ourking loc->
                    if curbox.type=="K":    
                        majesty(table,curbox)
                    moverecord=[lastbox,curbox]
        #special move
        if not (lastbox.specialnext is None):
            if len(lastbox.specialnext):
                if lastbox.type=="P":
                    if curbox.loc==lastbox.specialnext[0].loc:
                        mymove=move(lastbox,curbox)
                        mymove.movespecial(lastbox.specialnext)
                        curstep+=1
                        moverecord=[lastbox,curbox]
                if lastbox.type=="K":
                    for cstmv in lastbox.specialnext:
                        if curbox.loc==cstmv[0].loc:
                            mymove=move(lastbox,curbox)
                            mymove.movespecial(cstmv)
                            curstep+=1
                            majesty(table,curbox)
                            #<-renew ourking loc
                            moverecord=[lastbox,curbox]
                            break
            
    #recursion condition
    if curbox.loc=="a1":
        if not (lastbox is None):
            opt=rs.MessageBox("Are you sure to quit?",4)
            if opt==6:
                mysel.default(lastbox)
                return curbox
            else:
                select(curbox,table,curstep,moverecord)
    else:
        select(curbox,table,curstep,moverecord)
        
        
def loc_translate(i,j):
    #translate location i,j into standard record
    x=""
    y=""
    if i==1:
        x="a"
    elif i==2:
        x="b"
    elif i==3:
        x="c"
    elif i==4:
        x="d"
    elif i==5:
        x="e"
    elif i==6:
        x="f"
    elif i==7:
        x="g"
    elif i==8:
        x="h"
    else:
        print "error in location translate"
        return ERROR
    if j==1:
        y="1"
    elif j==2:
        y="2"
    elif j==3:
        y="3"
    elif j==4:
        y="4"
    elif j==5:
        y="5"
    elif j==6:
        y="6"
    elif j==7:
        y="7"
    elif j==8:
        y="8"
    else:
        print "error in location translate"
        return ERROR
    return x+y

class showmove:
    #show the possible next step in colors
    def en(self,box):
        mysel=dr.boxcolor()
        mysel.blue(box)
        return OK
    def eat(self,box):
        mysel=dr.boxcolor()
        mysel.red(box)
        return OK
    def de(self,table,i,j):
        mysel=dr.boxcolor()
        mysel.default(box)
        return OK

def opposite(curcolor):
    #to change the side of the chessmen
    if curcolor=="BLACK":
        newcolor="WHITE"
    elif curcolor=="WHITE":
        newcolor="BLACK"
    else:
        return ERROR
    return newcolor

def stepmonitor(curstep,box):
    #monitor the current step to make sure the right side to move
    if curstep%2==0 and box.menclr=="WHITE":
        return TRUE
    elif curstep%2==1 and box.menclr=="BLACK":
        return TRUE
    else:
        return FALSE
    
def callmen(table,i,j,lastmoverecord):
    #select a chessmen and show next move steps
    if table[i][j].type=="P":
        mypawn=chessmen.pawn(table,i,j,lastmoverecord)
        psbmove=mypawn.nextmove(table,i,j)
        mv=showmove()
        #standard move
        if len(psbmove.next):
            for movebox in psbmove.next:
                if table[i][j].menclr==opposite(movebox.menclr):
                    mv.eat(movebox)
                else:
                    mv.en(movebox)
        #en passant move
        if len(psbmove.specialnext):
            mv.eat(psbmove.specialnext[0])
        return table[i][j]
        
    if table[i][j].type=="B":
        mybishop=chessmen.bishop(table,i,j)
        psbmove=mybishop.nextmove(table,i,j)
        mv=showmove()
        if len(psbmove.next) :
            for movebox in psbmove.next:
                if table[i][j].menclr==opposite(movebox.menclr):
                    mv.eat(movebox)
                else:
                    mv.en(movebox)
        return table[i][j]
        
    if table[i][j].type=="R":
        myrook=chessmen.rook(table,i,j)
        psbmove=myrook.nextmove(table,i,j)
        mv=showmove()
        if len(psbmove.next):
            for movebox in psbmove.next:
                if table[i][j].menclr==opposite(movebox.menclr):
                    mv.eat(movebox)
                else:
                    mv.en(movebox)
        return table[i][j]
        
    if table[i][j].type=="Q":
        myqueen=chessmen.queen(table,i,j)
        psbmove=myqueen.nextmove(table,i,j)
        mv=showmove()
        if len(psbmove.next):
            for movebox in psbmove.next:
                if table[i][j].menclr==opposite(movebox.menclr):
                    mv.eat(movebox)
                else:
                    mv.en(movebox)
        return table[i][j]
    if table[i][j].type=="N":
        myknight=chessmen.knight(table,i,j)
        psbmove=myknight.nextmove(table,i,j)
        mv=showmove()
        if len(psbmove.next):
            for movebox in psbmove.next:
                if table[i][j].menclr==opposite(movebox.menclr):
                    mv.eat(movebox)
                else:
                    mv.en(movebox)
        return table[i][j]
        
    if table[i][j].type=="K":
        myking=chessmen.king(table,i,j)
        psbmove=myking.nextmove(table,i,j)
        mv=showmove()
        if not (psbmove.next is None) and len(psbmove.next):
            for movebox in psbmove.next:
                if table[i][j].menclr==opposite(movebox.menclr):
                    mv.eat(movebox)
                else:
                    mv.en(movebox)
        #castling move
        if (psbmove.specialnext is not None) and len(psbmove.specialnext):
            for cstmove in psbmove.specialnext:
                mv.en(cstmove[0])
        return table[i][j]
    else:
        return OK

class move:
    def __init__(self,curbox,nextbox):
        self.curbox=curbox
        self.nextbox=nextbox
        
    def movemen(self):
        #if not (self.nextbox.menclr is None):
        if self.nextbox.menclr==opposite(self.curbox.menclr):
            self.eat()
        else:
            self.standardmove()
            
        if self.nextbox.type=="P":
            #check whether the pawn is to upgrade
            self.uprising()
        
        return OK
        
    def movespecial(self,specialmove):
        #self:self, curbox:current box, nextbox:target box, specialmove:list of box
        #special move
        if self.curbox.type=="P" :
            if (self.curbox.col-self.nextbox.col)==0:
                #uprising
                self.uprising()
            elif abs(self.curbox.col-self.nextbox.col)==1:
                #enpassant:
                self.enpassant(specialmove)
            else:
                print "wtf???other special move???"
                return ERROR
        if self.curbox.type=="K":
            self.castling(specialmove)
        
        return OK
        
    def standardmove(self):
        #move the chessmen
        #transform matrix
        #xform=rs.XformTranslation(rs.VectorCreate(nextbox.cen,curbox.cen))
        #move to nextbox
        self.nextbox.menclr=self.curbox.menclr
        self.nextbox.type=self.curbox.type
        self.nextbox.ourking=self.curbox.ourking
        self.nextbox.chessmen=rs.MoveObjects(self.curbox.chessmen,rs.VectorCreate(self.nextbox.cen,self.curbox.cen))
        self.curbox.menclr=None
        self.curbox.type=None
        self.curbox.next=None
        self.curbox.ourking=None
        self.nextbox.step=self.curbox.step+1
        rs.DeleteObjects(self.curbox.chessmen)
        return self.curbox
        
    def eat(self):
        #eat opposite chessmen
        self.nextbox.menclr=self.curbox.menclr
        self.nextbox.type=self.curbox.type
        self.nextbox.ourking=self.curbox.ourking
        rs.UnlockObjects(self.nextbox.chessmen)
        rs.DeleteObjects(self.nextbox.chessmen)
        self.nextbox.chessmen=rs.MoveObjects(self.curbox.chessmen,rs.VectorCreate(self.nextbox.cen,self.curbox.cen))
        self.curbox.menclr=None
        self.curbox.type=None
        self.curbox.next=None
        self.curbox.ourking=None
        return self.curbox

    #special move for 0-0 and 0-0-0
    def castling(self,kingtargetloc):
        #kingtarget:type specialmove:[kingnext,rookcurrent,rooknext]
        
        kingnext=kingtargetloc[0]
        rookcur=kingtargetloc[1]
        rooknext=kingtargetloc[2]
        
        kingnext.menclr=self.curbox.menclr
        kingnext.type=self.curbox.type
        kingnext.chessmen=rs.MoveObjects(self.curbox.chessmen,rs.VectorCreate(kingnext.cen,self.curbox.cen))
        self.curbox.menclr=None
        self.curbox.type=None
        self.curbox.next=None
        kingnext.step=self.curbox.step+1
        
        rooknext.menclr=rookcur.menclr
        rooknext.type=rookcur.type
        rooknext.ourking=rookcur.ourking
        rooknext.chessmen=rs.MoveObjects(rookcur.chessmen,rs.VectorCreate(rooknext.cen,rookcur.cen))
        rookcur.menclr=None
        rookcur.type=None
        rookcur.next=None
        rookcur.ourking=None
        rooknext.step=rookcur.step+1
        
        return OK
        
    def enpassant(self,specialmove):
        #special move 'en passant'
        lastpawnbox=specialmove[1]
        targetbox=self.nextbox
        lastpawnbox.menclr=None
        lastpawnbox.type=None
        rs.UnlockObjects(lastpawnbox.chessmen)
        rs.DeleteObjects(lastpawnbox.chessmen)
        self.nextbox.menclr=self.curbox.menclr
        self.nextbox.type=self.curbox.type
        self.nextbox.ourking=self.curbox.ourking
        self.nextbox.chessmen=rs.MoveObjects(self.curbox.chessmen,rs.VectorCreate(self.nextbox.cen,self.curbox.cen))
        self.curbox.menclr=None
        self.curbox.type=None
        self.curbox.next=None
        self.curbox.ourking=None
        self.curbox.specialnext=None
        return OK
        
    def uprising(self):
        #special move when pawn reached the endline
        if self.nextbox.type=="P" and (self.nextbox.row==1 or self.nextbox.row==8):
            rs.MessageBox("pawn reached the end, choose your appointment")
            while 1:
                str=rs.GetString("make decision: Q=Queen,R=Rook,B=Bishop,N=Knight","Q")
                if str=="Q":
                    click=rs.MessageBox("Are you sure the pawn will change to: Queen?",4,"pawn promoted")
                    if click==6:break
                    if click==7:continue
                elif str=="R":
                    click=rs.MessageBox("Are you sure the pawn will change to: Rook?",4,"pawn promoted")
                    if click==6:break
                    if click==7:continue
                elif str=="B":
                    click=rs.MessageBox("Are you sure the pawn will change to: Bishop?",4,"pawn promoted")
                    if click==6:break
                    if click==7:continue
                elif str=="N":
                    click=rs.MessageBox("Are you sure the pawn will change to: Knight?",4,"pawn promoted")
                    if click==6:break
                    if click==7:continue
                else:
                    rs.MessageBox("error,please check your input(must be Q,R,B or N)",0,"error")
            self.nextbox.type=str
            rs.UnlockObjects(self.nextbox.chessmen)
            rs.DeleteObjects(self.nextbox.chessmen)
            newchessmen=dr.chessmen()
            self.nextbox.chessmen=newchessmen.volumn(self.nextbox)
        return OK
