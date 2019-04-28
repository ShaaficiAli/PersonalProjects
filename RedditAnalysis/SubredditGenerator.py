from matplotlib import pyplot as plt
import urllib3
import pprint
from bs4 import BeautifulSoup
from BotInfo import Bot
import sqlite3
import praw

def generateListOfSubreddits():
    url = "https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits"
    http = urllib3.PoolManager()
    response = http.request('GET',url)
    soup = BeautifulSoup(response.data,'lxml')
    subreddits = []
    for link in soup.find_all('a'):
        if "/r/" == link.get('href')[:3] and link.get('href').count('/')<3:
            subreddits.append(link.get('href'))
    
    subreddits = list(set(subreddits))
    subreddits.sort()
    return subreddits

def test():
    reddit = praw.Reddit(client_id=Bot.client_id,
                         client_secret=Bot.secret,
                         username=Bot.UserName,
                         password=Bot.Password,
                         user_agent = "A reddit parsing bot so I can do sentiment analysis on different subreddits."
                         )
    submission = reddit.submission(id='39zje0')
    redditor = reddit.redditor('Somali_Imhotep')
    comment = reddit.comment('dkk4qjd')
    print(submission.title)
    print(comment.created_utc)
    print(redditor.created_utc)
    pprint.pprint(vars(submission))
    print("///////////////////////////////////////////////////////////")
    pprint.pprint(vars(comment))
    print("///////////////////////////////////////////////////////////")
    pprint.pprint(vars(redditor))
    

def RedditDataBaseCreation():
    connection = sqlite3.connect()
    cursor = connection.cursor()
    tables = ['Subreddits','Posts','Redditors','Comments']
    SubredditTableSql = "CREATE table Subreddits (SubredditID int AUTOINCREMENT,Subscribers int, created Date,name varchar(50),primary key(SubredditID)) "
    
    RedditorTableSql = "CREATE table Redditor (RedditorID int AUTOINCREMENT,been_gilded BOOLEAN, created Date, name varchar(50),default_icon BOOLEAN,default_banner BOOLEAN, mod Boolean, link_karma int, comment_karma int, total AS link_karma+comment_karma, primary key(RedditorID))"
    
    PostsTableSql = "CREATE table Posts (PostID int AUTOINCREMENT,RedditorID int,SubredditID int,score int, upvoteratio float,downvotes int,gilded BOOLEAN, num_comment int, name varchar(300), over_18 BOOLEAN,  primary key(PostID),"
    "foreign key(SubredditID) references Subreddits(SubredditID) ON DELETE CASCADE, foreign key(SubredditID) references Subreddits(SubredditID) ON DELETE CASCADE"

    CommentsTableSql = "CREATE TABLE Comments(CommentID int AUTOINCREMENT,comment varchar(10000),karma int,ratio float,edited Boolean)"

    CommentsOnSql = "CREATE TABLE CommentsOn(CommentID int, PostID int,SubredditID int, RedditorID int, foreign key(CommentID) references Comments(CommentsID), foreign key(RedditorID) references Redditor(RedditorID), foreign key(SubredditID) references Subreddits(SubredditID), foreign key(CommentID) references Comments(CommentID))"

    FlairsTableSql = "CREATE TABLE Flairs(RedditorID int,SubredditID int, flair varchar(500), foreign key(RedditorID) references Redditors(RedditorID) ON DELETE CASCADE, foreign key(SubredditID) references Subreddits(SubredditID) ON DELETE CASCADE)"    
    #if cursor.execute
