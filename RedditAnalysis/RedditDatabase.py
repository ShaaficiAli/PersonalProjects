import matplotlib
import sqlite3
import praw
from BotInfo import Bot
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
getSubredditUserPostData('all',"RedditUsers.db")

       