from matplotlib import pyplot as plt
import sqlite3
import praw
from BotInfo import Bot
import datetime

#Custom errors for maxRedditors and maxSUbmissions param in getSubredditUsersPostData
class maxRedditorsException(Exception):
    pass
class maxSubmissionsException(Exception):
    pass

def getSubredditUserPostData(SubredditName,dbFileName,maxRedditor=25,maxSubmissions=500):
    """
        This function retrieves post history of redditors who post in SubredditName and stores the post title,which subreddit it was posted in, the utc date it was posted,
        the amount of likes it has and the name of the redditor. If a table for SubredditName has not been intialized and table will be created that has its name.
        Only Unique posts are retrieved.If the db file from dbFileName is not initialized then it will be created for you called dbFileName.
    """
    #Error checking to ensure that maxRedditor and maxSubmissions are integers between 0 and 1000 niclusive
    if not(isinstance(maxSubmissions,int) and not isinstance(maxSubmissions,float)):
        raise maxSubmissionsException("maxSubmissions must be and integer not "+str(type(maxSubmissions)))
    if not(isinstance(maxRedditor,int) and not isinstance(maxSubmissions,float)):
        raise maxRedditorsException("maxRedditor must be and integer not "+str(type(maxRedditor)))   
    if maxRedditor>1000 or maxRedditor<0:
        raise maxRedditorsException("maxRedditor must be between 0 and 1000 inclusive")
    if maxSubmissions>1000 or maxSubmissions<0:
        raise maxSubmissionsException("maxSubmissions must be between 0 and 1000 inclusive")
    
    #The Bot used is stored in another class file. The File is BotInfo use it if you want.
    reddit = praw.Reddit(client_id=Bot.client_id,
                         client_secret=Bot.secret,
                         username=Bot.UserName,
                         password=Bot.Password,
                         user_agent = "A reddit parsing bot so I can do sentiment analysis on different subreddits."
                         )
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    #If the table is not in the dbFileName then create it
    if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+SubredditName+
                      "'").fetchall()==[]:
        print("CREATING TABLE "+SubredditName)
        cursor.execute(" CREATE table '"+SubredditName+"' (id INTEGER PRIMARY KEY AUTOINCREMENT,subreddit TEXT,username TEXT,title TEXT,date INTEGER,karma INTEGER)")
    
    for submission in reddit.subreddit(SubredditName).hot(limit=maxSubmissions):
        redditor = submission.author
        #searching through the history of submitters from the subreddit given
        for post in redditor.submissions.new(limit=maxRedditor):
            date = int(post.created_utc)
            karma = post.score
            title = post.title
            sub = post.subreddit.display_name
            name = redditor.name
            item = (sub,name,title,date,karma,)
            sqlStatement = "SELECT subreddit, username, title, date FROM '"+SubredditName+"' WHERE subreddit = ? and username = ? and title = ? and date = ?"
            #if this particular post has not already been added to the subreddit then add it
            if cursor.execute(sqlStatement,(sub,name,title,date)).fetchall()==[]:
                cursor.execute("INSERT INTO '"+SubredditName+"' (subreddit,username,title,date,karma) VALUES(?,?,?,?,?)",item)
    connection.commit()
    connection.close()
    
def SubredditRedditorsPostDistributions(SubredditName,dbFileName):
    """
        This function returns a list of dates in the table given by SubredditName and changes the date item in each query item to how many days that post was before the most recent post.
        It also returns the name of the subreddit and how many days the entire table spans. 
    """
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
    """
        Creates a histogram from the data given by SubreddRedditorsPostDistributions(). If multiple sets of data are given then the histogram will compare and contrast those
        datasets and provide a legend for the color of each.The title will reflect which subreddits are given
    """
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
"""
if Post frequency froms users from 'The_Donald' and 'all' want to be put side by side for analysis then this is the way to use the code to do so. The db file is called RedditUsers.db
"""
getSubredditUserPostData("The_Donald","RedditUsers.db")
getSubredditUserPostData("all","RedditUsers.db")
data1 = SubredditRedditorsPostDistributions("The_Donald","RedditUsers.db")
data2 = SubredditRedditorsPostDistributions("all","RedditUsers.db")
displayHistogram(data1,data2)
  


       
