3###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules 
import rhinoscriptsyntax as rs
import scriptcontext as sc
import czy_chess_operator as op

#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

def opposite_move(table,i,j):
    #return possible capturing place of the current box
    box=table[i][j]
    if box.type=="P":
        newpsbms=[] 
        #thispawn=pawn(table,i,j,None)
        psbms=[]
        ###declude the straight walk of the pawn!!!!!#######
        #####only diagonal place is considered dangerous####
        if box.menclr=="WHITE":
            if i+1<8 and i-1>-1 and j+1<8:
                if table[i+1][j+1].menclr==None:
                    psbms.append(table[i+1][j+1])
                if table[i-1][j+1].menclr==None:
                    psbms.append(table[i-1][j+1])
        if box.menclr=="BLACK":
            if i+1<8 and i-1>-1 and j-1<8:
                if table[i+1][j-1].menclr==None:
                    psbms.append(table[i+1][j-1])
                if table[i-1][j-1].menclr==None:
                    psbms.append(table[i-1][j-1])
        newpsbms=psbms
        return newpsbms
    if box.type=="N":
        thisknight=knight(table,i,j)
        movebox=thisknight.allmove(table,i,j)
        psbms=movebox.next
        movebox.next=None
        if psbms is None:
            return []
        return psbms
    if box.type=="B":
        thisbishop=bishop(table,i,j)
        movebox=thisbishop.allmove(table,i,j)
        psbms=movebox.next
        movebox.next=None
        if psbms is None:
            return []
        return psbms
    if box.type=="R":
        thisrook=rook(table,i,j)
        movebox=thisrook.allmove(table,i,j)
        psbms=movebox.next
        movebox.next=None
        if psbms is None:
            return []
        return psbms
    if box.type=="Q":
        thisqueen=queen(table,i,j)
        movebox=thisqueen.allmove(table,i,j)
        psbms=movebox.next
        movebox.next=None
        if psbms is None:
            return []
        return psbms
    if box.type=="K":
        thisking=king(table,i,j)
        ###return the psbnextmove of the king rather than the secure move
        psbms=thisking.psbnextmove(table,i,j)
        if psbms is None:
            return []
        return psbms

def boxcompare(box1,box2):
    if box1.col==box2.col and box1.row==box2.row:
        return True
    else :
        return False
    

class king:
    def __init__(self,table,i,j):
        table[i][j].specialnext=None
        self.value=10                               #worth 10pt
        self.type="SHORT"                           #short weapon
        self.loc=table[i][j].loc                    #location
        self.color=table[i][j].menclr               #king color
        self.check=False                            #whether the king is checked
        self.checkby=[]                             #if checked ,check by whom
        self.cast=False                             #whether the king can castling
        self.castmove=None                          #store the castling move box
        #self.checkstatus(table,i,j)
        
    def psbnextmove(self,table,i,j):
        #regardless of potential check place the possible move of the king
        #to define the opposite king's moveplace
        psbms=[]
        for m in [-1,0,1]:
            for n in [-1,0,1]:
                if not (m==0 and n==0):
                    if i+m<8 and i+m>-1 and j+n<8 and j+n>-1:
                        if table[i+m][j+n].menclr!=table[i][j].menclr:
                            psbms.append(table[i+m][j+n])
        return psbms
        
    def nextmove(self,table,i,j):
        ###cannot move to checked place!!!###
        newpsbm=[]
        psbms=self.psbnextmove(table,i,j)
        checklist=self.checkstatus(table,i,j)
        if self.check==True:
            print "checked!"
        ###eliminate the dangerous(may be checked) zones from psb moves####
        #if possible move box is not checked, then it is secure and add to newpsbm list
        for psbm in psbms:
            ##if enemy unit already exists in the move range 
            ##define whether the current king can capture it
            if psbm.menclr!=self.color:
                #clear the existing box temporarily,define whether the box is under protection
                tmpclr=psbm.menclr
                tmptype=psbm.type
                psbm.menclr=None
                psbm.type=None
                checklist=self.checked(table,psbm,self.color)
                psbm.menclr=tmpclr
                psbm.type=tmptype
            else:
                checklist=self.checked(table,psbm,self.color)
            if not checklist[0]:
                newpsbm.append(psbm)
        #castling move for king and rook
        self.castmove=self.castling(table,i,j)
        table[i][j].next=newpsbm
        return table[i][j]
    
    def checkstatus(self,table,i,j):
        ##define whether the king is checked
        checklist=self.checked(table,table[i][j],self.color)
        if checklist[0]:
            self.check=True
            self.checkby=checklist[1]
    
    def castling(self,table,i,j):
        ##define whether the king is able to castling
        
        if i!=4:                return None
        if table[i][j].step!=0: 
            table[i][j].specialnext=None
            return None    #king had been moved
        if self.check==True:    return None    #king is checked
        moves=[]
        table[i][j].specialnext=[]
        #king side castling 0-0
        
        r1flag=True
        if table[0][j].type!="R":r1flag=False
        if table[0][j].step!=0: r1flag=False 
        #   if something exists in the interval then not able to 0-0
        if (table[5][j].type is not None) or (table[6][j].type is not None): r1flag=False
        checklist_k1=self.checked(table,table[5][j],self.color)
        checklist_k2=self.checked(table,table[6][j],self.color)
        #   if the interval space is underattack then not able to 0-0
        if checklist_k1[0]!=False and checklist_k2[0]!=False:r1flag=False
        if r1flag==True:
            moves.append(table[6][j])      #if can 0-0 ,add to movebox
            self.cast=True
            ##specialnext list:kingnext,rookcurrent,rooknext
            table[i][j].specialnext.append([table[6][j],table[7][j],table[5][j]])
        #queen side castling 0-0-0
        r2flag=True
        if table[7][j].type!="R":r2flag=False
        if table[7][j].step!=0: r2flag=False 
        #   if something exists in the interval then not able to 0-0
        if (table[1][j].type is not None) or (table[2][j].type is not None) or (table[3][j].type is not None): 
            r2flag=False
        checklist_q1=self.checked(table,table[4][j],self.color)
        checklist_q2=self.checked(table,table[3][j],self.color)
        #   if the interval space is underattack then not able to 0-0
        if checklist_q1[0]!=False and checklist_q2[0]!=False:r2flag=False
        if r2flag==True: 
            moves.append(table[2][j])  #if can 0-0-0,add to movebox
            self.cast=True
            ##specialnext list:kingnext,rookcurrent,rooknext
            table[i][j].specialnext.append([table[2][j],table[0][j],table[3][j]])
        return moves
        
    def checked(self,table,box,mycolor):
        #define whether the current box is checked
        """
        #method 1
        dgplaces=self.dangerous(table,i,j)
        for dgplace in dgplaces:
            if boxcompare(table[i][j],dgplace):
                print "CHECKED!!!!"
                return TRUE"""
        checkby=[]
        enemycolor=op.opposite(mycolor)
        checklist=[False,checkby]   #list[checked:bolean, bywhom:box list] if len(checklist[1])==0 then no one check

        for m in range(8):
            for n in range(8):
                if table[m][n].menclr==enemycolor:
                    moves=opposite_move(table,m,n)
                    if len(moves):
                        for move in moves:
                            if boxcompare(box,move):
                                checklist[0]=True
                                checklist[1].append(table[m][n])
        return checklist

def callchessmen(table,i,j):
    #different from op.callmen
    box1=None
    if table[i][j].type=="N":
        mymen=knight(table,i,j)
        box=mymen.allmove(table,i,j)
    if table[i][j].type=="R":
        mymen=rook(table,i,j)
        box=mymen.allmove(table,i,j)
    if table[i][j].type=="B":
        mymen=bishop(table,i,j)
        box=mymen.allmove(table,i,j)
    if table[i][j].type=="Q":
        mymen=queen(table,i,j)
        box=mymen.allmove(table,i,j)
    if table[i][j].type=="P":
        mymen=pawn(table,i,j,None)
        box=mymen.allmove(table,i,j)
        for move in box.next:
            print move.loc
    if table[i][j].type=="K":
        mymen=king(table,i,j)
    return box

def protectking(table,i,j):
    #if the king is checked return whether it can move or not
    protectmove=[]
    kingbox=table[i][j].ourking
    kx=kingbox.col-1
    ky=kingbox.row-1
    myking=king(table,kx,ky)
    myking.checkstatus(table,kx,ky)
    if myking.check==False:
        return -1
    #if our king is checked->
    if myking.check==True:
        print "check"
        box=callchessmen(table,i,j)
        #if doublecheck,i can do nothing
        if len(myking.checkby)>1:
            return []
        elif len(myking.checkby)==1:
            checker=myking.checkby[0]
            mvboxs=box.next
            if len(mvboxs)==0:return []
            for mvbox in mvboxs:
                #if can capture the checker->
                if mvbox.loc==checker.loc:
                    protectmove.append(mvbox)  
                    box.next=None
                #if can"stand" and cut off the attackline->
                thisEnemy=callchessmen(table,checker.col-1,checker.row-1)
                if thisEnemy.type=="R" or thisEnemy.type=="B" or thisEnemy.type=="Q":
                    #<--if long weapon
                    for nextmove in thisEnemy.next:
                        #possible defend place->
                        if mvbox==nextmove :
                            fmen=fakemen(mvbox,table[i][j].menclr)
                            fmen.deploy(mvbox)
                            newEnemy=callchessmen(table,checker.col-1,checker.row-1)
                            flag=True
                            for nextmove in newEnemy.next:
                                if nextmove.loc==kingbox.loc:
                                    flag=False
                            if flag==True:
                                #if successfully intercepted
                                protectmove.append(mvbox)  
                            fmen.destroy(mvbox)
        thisEnemy.next=None
        box.next=None           #<-important!!!!!
    return protectmove
    
class fakemen:
    #deploy or destroy a "fakemen" in currentbox
    def __init__(self,box,color):
        self.color=color
    def deploy(self,box):
        box.menclr=self.color                        
        box.type="P"     
        return box
    def destroy(self,box):
        box.menclr=None                      
        box.type=None   
        return box
        
class fakemove:
    #proceed a fake step in the table
    def __init__(self):
        pass
    def forward(self,curbox,nextbox):
        nextbox.menclr=curbox.menclr
        nextbox.type=curbox.type
        curbox.type=None
        curbox.menclr=None
    def eat(self,nextbox):
        tmptype=nextbox.type
        nextbox.menclr=None
        nextbox.type=None
        return tmptype
    def vormit(self,nextbox,type,color):
        nextbox.type=type
        nextbox.menclr=color

def movecheck(table,movebox):
    #check whether the move is available: prevent the explosure of ourking
    psbms=[]
    nextmvs=movebox.next
    if not nextmvs:
        return ERROR
        
    #instantiations->
    kingbox=movebox.ourking
    kx=kingbox.col-1
    ky=kingbox.row-1
    myking=king(table,kx,ky)
    myFakemove=fakemove()
    
    #check the move box->
    for nextmove in nextmvs:
        print nextmove.loc
        if nextmove.type is not None:
            tmptype=myFakemove.eat(nextmove)
            myking.check=False              #<-important! init check status
            myking.checkstatus(table,kx,ky)
            if myking.check==False:
                psbms.append(nextmove)
            myFakemove.vormit(nextmove,tmptype,op.opposite(movebox.menclr))
            continue
        myFakemove.forward(movebox,nextmove)
        myking.check=False              #<-important! init check status
        myking.checkstatus(table,kx,ky)
        if myking.check==False:
            psbms.append(nextmove)
        myFakemove.forward(nextmove,movebox)
    
    #special check
    
    if psbms:
        for psbm in psbms:
            print psbm.loc
    #<-try one step to makesure the king is safe
    movebox.next=psbms
    return movebox
    
##queen##
class queen:
    def __init__(self,table,i,j):
        self.value=9    #worth 3.5pt
        self.type="LONG"  #long weapon
        self.loc=table[i][j].loc #location
        
    def secureking(table,i,j):
        kingbox=table[i][j]
    
    def nextmove(self,table,i,j):
        mvbox=self.allmove(table,i,j)
        promove=protectking(table,i,j)
        if promove!=-1:
            mvbox.next=promove
            return mvbox
        moves=movecheck(table,mvbox)
        return moves
        
    def allmove(self,table,i,j):
        #return list of possible move location of the chessmen
        psbm=[]
        psbm1=self.search(table,i,j,1,0,table[i][j].menclr)
        psbm2=self.search(table,i,j,-1,0,table[i][j].menclr)
        psbm3=self.search(table,i,j,0,-1,table[i][j].menclr)
        psbm4=self.search(table,i,j,0,1,table[i][j].menclr)
        psbm5=self.search(table,i,j,1,1,table[i][j].menclr)
        psbm6=self.search(table,i,j,1,-1,table[i][j].menclr)
        psbm7=self.search(table,i,j,-1,-1,table[i][j].menclr)
        psbm8=self.search(table,i,j,-1,1,table[i][j].menclr)
        if psbm1:psbm.extend(psbm1)
        if psbm2:psbm.extend(psbm2)
        if psbm3:psbm.extend(psbm3)
        if psbm4:psbm.extend(psbm4)
        if psbm5:psbm.extend(psbm5)
        if psbm6:psbm.extend(psbm6)
        if psbm7:psbm.extend(psbm7)
        if psbm8:psbm.extend(psbm8)
        if psbm:
            table[i][j].next=psbm
        else:
            table[i][j].next=[]
        return table[i][j]
                        
    def search(self,table,i,j,stepx,stepy,defcolor):
        #search for the possible move line by recursion
        #self,table:table,i:i,j:j,stepx:search step in x,stepy:search step in y, 
        #\defcolor:the origin color of selected bishop
        psbm=[]
        if not (i+stepx<8 and i+stepx>-1 and j+stepy<8 and j+stepy>-1):
            #if out of range
            return OK
        if table[i+stepx][j+stepy].type is None:
            psbm.append(table[i+stepx][j+stepy])
            psbm1=self.search(table,i+stepx,j+stepy,stepx,stepy,defcolor)
            if psbm1:
                psbm.extend(psbm1)
        elif table[i+stepx][j+stepy].menclr==defcolor:
            psbm=[]
            return psbm
        else:
            psbm.append(table[i+stepx][j+stepy])
            return psbm
        return psbm

##rook##
class rook:
    def __init__(self,table,i,j):
        self.value=5    #worth 3.5pt
        self.type="LONG"  #long weapon
        self.loc=table[i][j].loc #location
        
    def nextmove(self,table,i,j):
        mvbox=self.allmove(table,i,j)
        promove=protectking(table,i,j)
        if promove!=-1:
            mvbox.next=promove
            return mvbox
        moves=movecheck(table,mvbox)
        return moves
        
    def allmove(self,table,i,j):
        #return list of possible move location of the chessmen
        psbm=[]
        psbm1=self.search(table,i,j,1,0,table[i][j].menclr)
        psbm2=self.search(table,i,j,-1,0,table[i][j].menclr)
        psbm3=self.search(table,i,j,0,-1,table[i][j].menclr)
        psbm4=self.search(table,i,j,0,1,table[i][j].menclr)
        if psbm1:psbm.extend(psbm1)
        if psbm2:psbm.extend(psbm2)
        if psbm3:psbm.extend(psbm3)
        if psbm4:psbm.extend(psbm4)
        if psbm:
            table[i][j].next=psbm
        else:
            table[i][j].next=[]
        return table[i][j]
                        
    def search(self,table,i,j,stepx,stepy,defcolor):
        #search for the possible move line by recursion
        #self,table:table,i:i,j:j,stepx:search step in x,stepy:search step in y, 
        #\defcolor:the origin color of selected bishop
        psbm=[]
        if not (i+stepx<8 and i+stepx>-1 and j+stepy<8 and j+stepy>-1):
            #if out of range
            return OK
        if table[i+stepx][j+stepy].type is None:
            psbm.append(table[i+stepx][j+stepy])
            psbm1=self.search(table,i+stepx,j+stepy,stepx,stepy,defcolor)
            if psbm1:
                psbm.extend(psbm1)
        elif table[i+stepx][j+stepy].menclr==defcolor:
            psbm=[]
            return psbm
        else:
            psbm.append(table[i+stepx][j+stepy])
            return psbm
        return psbm
        
##bishop##
class bishop:
    def __init__(self,table,i,j):
        self.value=3.5    #worth 3.5pt
        self.type="LONG"  #long weapon
        self.loc=table[i][j].loc #location
    
    def nextmove(self,table,i,j):
        mvbox=self.allmove(table,i,j)
        promove=protectking(table,i,j)
        if promove!=-1:
            mvbox.next=promove
            return mvbox
        moves=movecheck(table,mvbox)
        return moves
        
    def allmove(self,table,i,j):
        #return list of possible move location of the chessmen
        psbm=[]
        psbm1=self.search(table,i,j,1,1,table[i][j].menclr)
        psbm2=self.search(table,i,j,1,-1,table[i][j].menclr)
        psbm3=self.search(table,i,j,-1,-1,table[i][j].menclr)
        psbm4=self.search(table,i,j,-1,1,table[i][j].menclr)
        if psbm1:psbm.extend(psbm1)
        if psbm2:psbm.extend(psbm2)
        if psbm3:psbm.extend(psbm3)
        if psbm4:psbm.extend(psbm4)
        if psbm:
            table[i][j].next=psbm
        else:
            table[i][j].next=[]
        return table[i][j]
       
                        
    def search(self,table,i,j,stepx,stepy,defcolor):
        #search for the possible move line by recursion
        #self,table:table,i:i,j:j,stepx:search step in x,stepy:search step in y, 
        #\defcolor:the origin color of selected bishop
        psbm=[]
        if not (i+stepx<8 and i+stepx>-1 and j+stepy<8 and j+stepy>-1):
            #if out of range
            return OK
        if table[i+stepx][j+stepy].type is None:
            psbm.append(table[i+stepx][j+stepy])
            psbm1=self.search(table,i+stepx,j+stepy,stepx,stepy,defcolor)
            if psbm1:
                psbm.extend(psbm1)
        elif table[i+stepx][j+stepy].menclr==defcolor:
            psbm=[]
            return psbm
        else:
            psbm.append(table[i+stepx][j+stepy])
            return psbm
        return psbm
        
##knight##
class knight:
    def __init__(self,table,i,j):
        self.value=3.5    #worth 3.5pt
        self.type="SHORT" #short weapon
        self.loc=table[i][j].loc #location
    
    def nextmove(self,table,i,j):
        mvbox=self.allmove(table,i,j)
        #return list of possible move location of the chessmen
        promove=protectking(table,i,j)
        if promove!=-1:
            mvbox.next=promove
            return mvbox
        moves=movecheck(table,mvbox)
        return moves
    
    def allmove(self,table,i,j):
        mv1=[-1,1,-2,2]
        psbm=[]
        for m in mv1:
            for n in mv1:
                if abs(m)!=abs(n):
                #only makes knight jump 2-1 step rather than 2-2 or 1-1
                    if (i+m)<8 and (i+m)>-1 and (j+n)<8 and (j+n)>-1:
                        if table[i+m][j+n].menclr!=table[i][j].menclr:
                        #not the same color of chessmen
                            psbm.append(table[i+m][j+n])
        table[i][j].next=psbm
        return table[i][j]

##pawn##
class pawn:
    def __init__(self,table,i,j,lastmoverecord):
        self.value=1                    #worth 1pt
        self.type="SHORT"               #short weapon
        self.loc=table[i][j].loc        #location
        self.lastmove=lastmoverecord    #record the last move for en passant
    
    def nextmove(self,table,i,j):
        moves=self.allmove(table,i,j)
        promv=protectking(table,i,j)
        if promv==-1:
            moves=movecheck(table,table[i][j])
            return moves
        else:
            table[i][j].next=promv
            return table[i][j]
        
    def allmove(self,table,i,j):
        #return list of possible move location of the chessmen
        psbm=[]
        if table[i][j].menclr=="WHITE":
            moves=self.white(table,i,j)
            psbm.extend(moves[0])
            psbm.extend(moves[1])
        elif table[i][j].menclr=="BLACK":
            moves=self.black(table,i,j)
            psbm.extend(moves[0])
            psbm.extend(moves[1])
        else:
            print "wtf?"
            return ERROR
        table[i][j].next=psbm
        return table[i][j]
    
    def white(self,table,i,j):
        #whitemove
        psbm=[]     #standardmove
        spcmv=[]    #specialmove- 'en passant'
        eatmv=[]    #capture move diagonal
        #move
        if table[i][j].step==0:
            #if it is the first time for pawn to move, it can jump 2 slots
            #if step=0 the pawn is at line 2 thus j==1 for sure, no need to determine
            if table[i][j+1].menclr is None:
                psbm.append(table[i][j+1])
                if table[i][j+2].menclr is None:
                    psbm.append(table[i][j+2])
        else:
            if j+1<8 and table[i][j+1].menclr is None:
                psbm.append(table[i][j+1])
        
        #standardeat
        if i+1<8 and j+1<8:
            if table[i+1][j+1].menclr==op.opposite(table[i][j].menclr):
                eatmv.append(table[i+1][j+1])
        if i-1>-1 and j+1<8:
            if table[i-1][j+1].menclr==op.opposite(table[i][j].menclr):
                eatmv.append(table[i-1][j+1])
        #eatpassby
        passbybox=self.eatpassby(table,i,j,self.lastmove)
        if passbybox:
            print "YES"
            spcmv=passbybox
        table[i][j].specialnext=spcmv
        """totalmv.extend(psbm)
        totalmv.extend(eatmv)
        table[i][j].next=totalmv"""
        return [psbm,eatmv]
        
    def black(self,table,i,j):
        #blackmove
        psbm=[]     #standardmove
        spcmv=[]    #specialmove- 'en passant'
        eatmv=[]    #capture move diagonal
        if table[i][j].step==0:
            #if it is the first time for pawn to move, it can jump 2 slots
            #if step=0 the pawn is at line 2 thus j==6 for sure, no need to determine
            if table[i][j-1].menclr is None:
                psbm.append(table[i][j-1])
                if table[i][j-2].menclr is None:
                    psbm.append(table[i][j-2])
        else:
            if j-1<8 and table[i][j-1].menclr is None:
                psbm.append(table[i][j-1])
        #standardeat
        if i+1<8 and j-1<8:
            if table[i+1][j-1].menclr==op.opposite(table[i][j].menclr):
                eatmv.append(table[i+1][j-1])
        if i-1>-1 and j-1<8:
            if table[i-1][j-1].menclr==op.opposite(table[i][j].menclr):
                eatmv.append(table[i-1][j-1])
        #eatpassby
        passbybox=self.eatpassby(table,i,j,self.lastmove)
        if passbybox:
            print "YES"
            spcmv=passbybox
        
        table[i][j].specialnext=spcmv
        return [psbm,eatmv]
    
    def eatpassby(self,table,i,j,lastmoverecord):
        #whether current chessmen can do special move 'en passant'
        #return a list [targetmove box, enemy passant box]
        if lastmoverecord is None:
            return False
        laststbox=lastmoverecord[0]
        lastedbox=lastmoverecord[1]
        spcmov=[]
        if lastedbox.type=="P" and abs(lastedbox.col-table[i][j].col)==1 and \
        abs(lastedbox.row-laststbox.row)==2 and table[i][j].row==lastedbox.row:
            spcmov.append(table[lastedbox.col-1][((lastedbox.row-1)+(laststbox.row-1))/2])
            spcmov.append(lastedbox)
            return spcmov
        return False

