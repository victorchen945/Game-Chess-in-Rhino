###########################               
#script by Zhengyang Chen #        
#tel: +86 13818034245     #
#wechat: czy4050715       #
#########    +1s   ########
###########################


#import rhino modules 
import rhinoscriptsyntax as rs
import scriptcontext as sc

#import chess modules
import czy_chesstable as tb
import czy_chess_render as dr
from czy_chess_operator import select


#defines

OK=0
ERROR=-1
TRUE=1
FALSE=0
OVERFLOW=-2




def main():
    rs.AddLayer("chessmen")
    mytable=tb.init_table()
    table=mytable.storebox()
    
    select(None,table,0,None)
    
main()
