###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules 
import rhinoscriptsyntax as rs
import scriptcontext as sc

import czy_chess_render as dr
import czy_chess_operator as op
import czy_chessmen as chessmen

#defines
OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2

SCALE=10

BLACK=1
WHITE=0

NONE=None

#chess table of 8*8
class init_table:
    
    def __init__(self):
        self.table=[[0 for i in range(8)]for j in range(8)]
        
    def storebox(self):
        #store the information of each cell of the table 
        for i in range(8):
            for j in range(8):
                mybox=box(i+1,j+1)
                if j==0:
                    mybox=self.storechessmen_major(mybox,i,"WHITE")
                elif j==1:
                    mybox=self.storechessmen_minor(mybox,"WHITE")
                elif j==6:
                    mybox=self.storechessmen_minor(mybox,"BLACK")
                elif j==7:
                    mybox=self.storechessmen_major(mybox,i,"BLACK")
                else: 
                    pass
                self.table[i][j]=mybox
        op.majesty(self.table,self.table[4][0])
        op.majesty(self.table,self.table[4][7])
        self.display()
        return self.table
    
    def storechessmen_major(self,box,i,color):
        #store the major chessmen
        box.menclr=color
        if i==0 or i==7:
            box.type="R"     #rook
        elif i==1 or i==6: 
            box.type="N"    #knight
        elif i==2 or i==5:
            box.type="B"    #bishop
        elif i==3:
            box.type="Q"    #queeen
        elif i==4:
            box.type="K"    #king
        return box
        
    def storechessmen_minor(self,box,color):
        #store the pawns
        box.menclr=color
        box.type="P"
        return box
    
    def display(self):
        
        mytable=dr.chesstable()
        mytable.table(self.table)
        men=dr.chessmen()
        for i in range(8):
            for j in range(8):
                self.table[i][j].cen=self.table[i][j].cendroid()
                men.volumn(self.table[i][j])
        return OK
    
        
        

#single box in the table
class box:
    def __init__(self,col,row):
        self.col=col                            #1 to 8
        self.row=row                            #1 to 8
        self.menclr=NONE                        #BLACK,WHITE OR NULL
        self.type=NONE                          #K Q R B N P or NULL
        self.loc=op.loc_translate(col,row)      #location in standard record mode
        self.baseclr=self.color()               #BLACK or WHITE
        self.cell=NONE                          #display, the box surface selectable
        self.cen=self.cendroid()                #the cendroid point of the box  
        self.next=None                          #list of possible nextmove box ,just like linklist
        self.specialnext=None                   #special move like enpassant or castling
        self.chessmen=None                      #chessmen object
        self.step=0                             #record how many steps current chessmen(if exists) had been moved
        self.moved=False                        #define whether the current chessmen had been moved in last round
        self.ourking=None                       #define the friendly king box
        
        
    def color(self):
            if (self.col+self.row)%2==0:
                return "BLACK"
            elif (self.col+self.row)%2==1:
                return "WHITE"
            else:
                print "error in boxcolor"
                return ERROR
                
    def cendroid(self):
        if self.cell is None:
            return None
        if rs.IsSurface(self.cell):
            cenpt=rs.SurfaceAreaCentroid(self.cell)
            return cenpt[0]
        return None