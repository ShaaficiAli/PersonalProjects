import requests
import re
import json
import sqlite3
import time
from tft_utils import *
#the current patch update was dec 14 so matches collected will be from dec 16 upwards
epochtimestamp = 1671166800           

c,i,t = create_tft_dictionaries()
con = sqlite3.connect("Data/league_match.db")
cur = con.cursor()
cur.execute("select * from placements")
placements = cur.fetchall()




for place in placements:
    
    
    unitquery = "select * from units where placement_id="+str(place[0])
    cur.execute(unitquery)
    units = cur.fetchall()
    unitnames = [unit[0] for unit in units if unit[0] != None]
    
    firstitems = [unit[2] for unit in units if unit[2] != None]
    seconditems = [unit[3] for unit in units if unit[3] != None]
    thirditems = [unit[4] for unit in units if unit[4] != None]

    augments = [augment for augment in place[1:4] if augment!= None]
       
    items = firstitems+seconditems+thirditems
    
    
    comp = calculate_comp_traits(unitnames,items,augments,c,i,t)
    
    for compkey in comp.keys():
        num_units = comp[compkey]
        trait = compkey
        min_units,tier = calculate_trait_tier(num_units,trait,t)
       
        if min_units!=0:
            traits = [trait,num_units,min_units,tier,place[0]]
            
            cur.execute("INSERT INTO traits values(?,?,?,?,?)",traits)
con.commit()


    
            
   
    
