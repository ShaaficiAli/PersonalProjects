import sqlite3
import pickle
import json
con = sqlite3.connect("league_match.db")
cur = con.cursor()
cur.execute('select distinct(augments) from (Select first_augment as augments from placements Union all Select second_augment as augments from placements Union all select third_augment as augments from placements);')
augments = [augment[0] for augment in cur.fetchall()]
with open('augmetlist.pkl', 'wb') as f:
    pickle.dump(augments,f)
