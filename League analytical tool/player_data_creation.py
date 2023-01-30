import requests
import re
import json
import sqlite3
import time
import apikey
#player data first due to how the league api is set up
print("starting program at "+str(time.ctime()))
apikey = get_api_key()
con = sqlite3.connect("Data/league_match.db")
cur = con.cursor()
playertable = "CREATE TABLE players (puuid varchar(100),summonerID varchar(100),rank varchar(25),region varchar(10),wins int,losses int,leaguePoints int,summonerName varchar(255),veteran boolean,hotStreak boolean,freshBlood boolean,inactive boolean,primary key(puuid,summonerID));"
try:
    cur.execute(playertable)
except(sqlite3.OperationalError):
    pass

regions = ['na1','kr','jp1','eun1','euw1']
ranks = ["challenger","grandmaster"]


for rank in ranks:
    for region in regions:
        playerRequest = "https://"+region+".api.riotgames.com/tft/league/v1/"+rank+"?"+apikey
        players = json.loads(requests.get(playerRequest).text)['entries']
        for player in players:
            
            playerSummonerID = player['summonerId']
            PlayerInfo =json.loads(requests.get("https://"+region+".api.riotgames.com/tft/summoner/v1/summoners/"+playerSummonerID+"?"+apikey).text)
            puuid = PlayerInfo['puuid']
            playerwins = player['wins']
            playerloses = player['losses']
            leaguepoints = player['leaguePoints']
            name = player['summonerName']
            veteran = player['veteran']
            hotstreak = player['hotStreak']
            freshBlood = player['freshBlood']
            inactive = player['inactive']            
            accountid = PlayerInfo['accountId']
            profileIcon = PlayerInfo['profileIconId']
            summonerLevel = PlayerInfo['summonerLevel']
            datapoint = [puuid,playerSummonerID,rank,region,playerwins,playerloses,leaguepoints,name,veteran,hotstreak,freshBlood,inactive]
            try:
                cur.execute("INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",datapoint)
            except:
                print("duplicate from the league server")
            time.sleep(1.2)
        print('completed %s %s'%(rank,region))
print("commiting data at "+str(time.ctime()))
cur.commit()
cur.close()
con.close()
            
            
            



