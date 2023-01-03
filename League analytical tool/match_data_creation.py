import requests
import re
import json
import sqlite3
import time
#the current patch update was dec 14 so matches collected will be from dec 16 upwards
epochtimestamp = 1671166800

con = sqlite3.connect("Data/league_match.db")
cur = con.cursor()

placementTable = """CREATE TABLE placements(
placement_id integer primary key,
first_augment varchar(100),
second_augment varchar(100),
third_augment varchar(100),
matchid varchar(200),
placement int,
companion varchar(100),
gold_left int,
last_round int,
level int,
players_eliminated int,
puuid varchar(100),
time_eliminated float,
total_damage_to_players int,
foreign key(matchid) references matches);"""


unitTables = """CREATE TABLE units(
unitname varchar(100),
placement_id integer,
firstitem varchar(100),
seconditem varchar(100),
thirditem varchar(100),
tier int,
rarity int,
foreign key(placement_id) references placements);"""

traitTables = """CREATE TABLE traits(
traitname varchar(100),
num_units int,
tier_current int,
tier_total int,
placement_id integer,
foreign key(placement_id) references placements);"""

matchTables = """CREATE TABLE matches(
matchid varchar(100),
game_length float,
game_datetime float,
game_version varchar(200),
tft_game_type varchar(200),
tft_set_core_name varchar(200)
"""
#cur.execute(unitTables)
#cur.execute(placementTable)
cur.execute(matchTables)
cur.execute("SELECT puuid,region from players")
puuids = cur.fetchall()
for result in puuids:
    player = result[0]
    region = result[1]
    regionpart = ""
    if region in ['jp1','kr']:
        regionpart = "asia"
    elif region in ['eun1','euw1']:
        regionpart = "europe"
    else:
        regionpart = "americas"
    matchlistquery = "https://"+regionpart+".api.riotgames.com/tft/match/v1/matches/by-puuid/"+player+"/ids?start=0&startTime="+str(epochtimestamp)+"&count=20&"+apikey
    
    matches = json.loads(requests.get(matchlistquery).text)
    
    for match in matches:
        matchquery = "https://"+regionpart+".api.riotgames.com/tft/match/v1/matches/"+match+"/?"+apikey
        matchdata = json.loads(requests.get(matchquery).text)
        print(matchdata)
        #insert match values into match table
        matchid = match
        match_game_length = matchdata['info']['game_length']
        match_game_datetime = matchdata['info']['game_datetime']
        match_game_version = matchdata['info']['game_version']
        match_game_type = matchdata['info']['tft_game_type']
        match_game_set_core_name = matchdata['info']['tft_set_core_name']
        matchdatapoint = [matchid,
                          match_game_length,
                          match_game_datetime,
                          match_game_version,
                          match_game_type,
                          match_game_set_core_name]
        
        cur.execute("INSERT INTO matches values (?,?,?,?,?,?)",matchdatapoint)
        #get the players per match ad put their data in the placement table
        placements = matchdata['info']['participants']
        for placement in placements:
            placementid =
            try:
                if "augments" in placement:
                    first_augment = placement['augments'][0]
                else:
                    first_augment = None
            except:
                first_augment = None
            try:
                if "augments" in placement and len(placement['augments']>=2:
                    second_augment = placement['augments'][1]
                else:
                    second_augment = None
            
            else:
                second_augment = None
            try:
                if "augments" in placement and len(placement['augments']>=3:
                    third_augment = placement['augments'][2]
                else:
                    third_augment = None
            
            else:
                third_augment = None
             
            place = placement['placement']
            companion = placement['companion']['species']
            gold_left = placement['gold_left']
            last_round = placement['last_round']
            level = placement['level']
            player_eliminated = placement['players_eliminated']
            puuid = placement['puuid']
            time_eliminated = placement['time_eliminated']
            total_damage_to_players = placement['total_damage_to_players']
            placementdatapoint = [placementid,
                                  first_augment,
                                  second_augment,
                                  third_augment,
                                  matchid,
                                  place,
                                  companion,
                                  gold_left,
                                  last_round,
                                  level,
                                  player_eliminated,
                                  puuid,
                                  time_eliminated,
                                  total_damage_to_players]
                                  
            cur.execute("INSERT INTO placements values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",placementdatapoint)
            units = placement['units']
            for unit in units:
                unit_name = unit['character_id']
                try:
                    
                except:
                    pass
                try:
                    pass
                except:
                    pass
                try:
                    pass
                except:
                    pass
                
                unit_datapoint = [unit_name,
                                  first_item,
                                  second_item,
                                  third_item,
                                  
