from matplotlib import pyplot as plt
import sqlite3
#import praw
from BotInfo import Bot
import datetime
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
    posts=[]
    
    for submission in reddit.subreddit(SubredditName).hot(limit=maxSubmissions):
        redditor = submission.author
        for post in redditor.submissions.new(limit=maxRedditor):
            date = int(post.created_utc)
            karma = post.score
            title = post.title
            sub = post.subreddit.display_name
            name = redditor.name
            item = (sub,name,title,date,karma,)
            posts.append(item)
    cursor.executemany("INSERT INTO '"+SubredditName+"' (subreddit,username,title,date,karma) VALUES(?,?,?,?,?)",posts)
    connection.commit()
    connection.close()
    
def SubredditRedditorsPostDistributions(SubredditName,dbFileName):
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    Maximum = cursor.execute("SELECT MAX(date) FROM '"+SubredditName+"'").fetchone()[0]
    data = []
    for datapoint in cursor.execute("SELECT date FROM '"+SubredditName+"' ORDER BY date DESC"):
        utc_time = datapoint[0]
        item = (datetime.date.fromtimestamp(utc_time)-datetime.date.fromtimestamp(Maximum)).days
        data.append(abs(item))
    print(len(data))
    return data

def displayHistogram(*args):
    for data in args:
        plt.hist(data,1000,cumulative = True,density = True,alpha = 0.5)
    plt.show()
    
data1 = SubredditRedditorsPostDistributions("The_Donald","RedditUsers.db")
data2 = SubredditRedditorsPostDistributions("all","RedditUsers.db")
displayHistogram(data1,data2)
    


       
