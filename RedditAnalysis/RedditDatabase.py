from matplotlib import pyplot as plt
import sqlite3
import praw
from BotInfo import Bot
import datetime
import numpy as np
def getSubredditUserPostData(SubredditName,dbFileName,maxRedditor=25,maxSubmissions=500):
    reddit = praw.Reddit(client_id=Bot.client_id,
                         client_secret=Bot.secret,
                         username=Bot.UserName,
                         password=Bot.Password,
                         user_agent = "A reddit parsing bot so I can do sentiment analysis on different subreddits."
                         )
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+SubredditName+
                      "'").fetchall()==[]:
        print("CREATING TABLE "+SubredditName)
        cursor.execute(" CREATE table '"+SubredditName+"' (id INTEGER PRIMARY KEY AUTOINCREMENT,subreddit TEXT,username TEXT,title TEXT,date INTEGER,karma INTEGER)")
    
    for submission in reddit.subreddit(SubredditName).hot(limit=maxSubmissions):
        redditor = submission.author
        for post in redditor.submissions.new(limit=maxRedditor):
            date = int(post.created_utc)
            karma = post.score
            title = post.title
            sub = post.subreddit.display_name
            name = redditor.name
            item = (sub,name,title,date,karma,)
            sqlStatement = "SELECT subreddit, username, title, date FROM '"+SubredditName+"' WHERE subreddit = ? and username = ? and title = ? and date = ?"
            print(sqlStatement)
            if cursor.execute(sqlStatement,(sub,name,title,date)).fetchall()==[]:
                print("Sucess")
                cursor.execute("INSERT INTO '"+SubredditName+"' (subreddit,username,title,date,karma) VALUES(?,?,?,?,?)",item)
    connection.commit()
    connection.close()
    
def SubredditRedditorsPostDistributions(SubredditName,dbFileName):
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    Maximum = cursor.execute("SELECT MAX(date) FROM '"+SubredditName+"'").fetchone()[0]
    Minimum = cursor.execute("SELECT MIN(date) FROM '"+SubredditName+"'").fetchone()[0]
    duration = (datetime.date.fromtimestamp(Maximum)-datetime.date.fromtimestamp(Minimum)).days
    
    data = []
    for datapoint in cursor.execute("SELECT date FROM '"+SubredditName+"' ORDER BY date DESC"):
        utc_time = datapoint[0]
        item = (datetime.date.fromtimestamp(utc_time)-datetime.date.fromtimestamp(Maximum)).days
        data.append(abs(item))
    return [data,SubredditName,duration]

def displayHistogram(*args):
    subredditsInvolved = ""
    moreThanOne = len(args)>1
    for data in args:
        plt.hist(data[0],data[2],cumulative = True,density = True,alpha = 0.5,label = data[1],histtype='stepfilled')
        if data in args[1:-1] and moreThanOne:
            subredditsInvolved+=","+data[1]
        if data == args[-1] and moreThanOne:
            subredditsInvolved +=" and "+data[1]
        else:
            subredditsInvolved+=data[1]
            
    plt.legend(loc = 'upper right')
    plt.title("Comparison of postings frequencies from redditors from subreddits "+subredditsInvolved)
    plt.xlabel("Days before newest post")
    plt.ylabel("Cumulative distribution function of posts prior to most recent")
    plt.show()

getSubredditUserPostData("The_Donald","RedditUsers.db")
getSubredditUserPostData("all","RedditUsers.db")
data1 = SubredditRedditorsPostDistributions("The_Donald","RedditUsers.db")
data2 = SubredditRedditorsPostDistributions("all","RedditUsers.db")
displayHistogram(data1,data2)
    


       
