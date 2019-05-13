from matplotlib import pyplot as plt
import urllib3
import pprint
from bs4 import BeautifulSoup
from BotInfo import Bot
import sqlite3
import praw
from datetime import datetime

def generateListOfSubreddits(limitSubreddits):
    '''
    Generate as large a list as possible of top subreddits
    Keyword Arguments:
    limitSubreddits -- either an integer that states the amount of subreddits
    you want the list to contain or None which will generate as much subreddits as
    possible via reddit object limitiations
    '''
    #reddit object that will interact with reddit
    reddit = praw.Reddit(client_id=Bot.client_id,
                         client_secret=Bot.secret,
                         username=Bot.UserName,
                         password=Bot.Password,
                         user_agent = "A reddit parsing bot so I can do sentiment analysis on different subreddits."
                         )
    ls = []
    #iterate through the subreddits and append them to ls
    for subreddit in praw.models.Subreddits(reddit, None).popular(limit = limitSubreddits):
        print(subreddit.display_name)
        ls.append(subreddit.display_name)
        
    
    return ls
    

def RedditDataBaseCreation(dbFileName):
    '''
    Creates 5 tables in the database Comments,Posts,Submissions,Flairs,Subreddits
    along with their dependencies and constraints.
    
    Keyword arguments:
    dbFileName: the name of the sqlite database file that the tables and data
    will be in. Include path if the file is not in the same folder.

    Returns None
    
    '''
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    #allows foreigns keys to be implemented
    cursor.execute("PRAGMA foreign_keys = ON")
    #sql statements for each table
    SubredditTableSql = "CREATE table Subreddits (SubredditID INTEGER ,Subscribers int, created TIMESTAMP,name varchar(500),title varchar(500),description  varchar(10000),subRedditType varchar(200),advertiserCategory varchar(200),adultContent BOOLEAN,publicTraffic BOOLEAN,quarantined BOOLEAN,spoilersEnabled BOOLEAN,restrictPosting BOOLEAN,restrictComments BOOLEAN,allowImages BOOLEAN,allowDiscovery BOOLEAN,allowVideogifs BOOLEAN,allowVideos BOOLEAN,OnlyOriginalContent BOOLEAN,linkFlairs BOOLEAN,userFlairs BOOLEAN,primary key(SubredditID)) "
    
    RedditorTableSql = "CREATE table Redditor (RedditorID INTEGER ,isGold BOOLEAN, created TIMESTAMP, name varchar(50),description varchar(10000), mod Boolean, link_karma int, comment_karma int, totalKarma int,bannerImg varchar(1000),bannerX int, bannerY int,over18 BOOLEAN,default_icon BOOLEAN,default_banner BOOLEAN,employee BOOLEAN,verifiedEmail BOOLEAN, primary key(RedditorID))"
    
    PostsTableSql = "CREATE table Posts (PostID INTEGER ,RedditorID INTEGER,SubredditID INTEGER,permalink varchar(1000),score int, upvoteratio float,silver int, gold int,platinum int,totalAwards int,num_crossposts int, num_comment int, title varchar(300),created TIMESTAMP,edited BOOLEAN,spoiler BOOLEAN,stickied BOOLEAN, over_18 BOOLEAN,locked BOOLEAN,is_meta BOOLEAN,is_original_content BOOLEAN, primary key(PostID),foreign key(RedditorID) references Redditor(RedditorID) ON DELETE CASCADE ON UPDATE CASCADE, foreign key(SubredditID) references Subreddits(SubredditID) ON DELETE CASCADE ON UPDATE CASCADE)"

    CommentsTableSql = "CREATE TABLE Comments(PostID INTEGER,CommentID INTEGER ,SubredditID int, RedditorID int,comment varchar(10000),permalink varchar(1000),created TIMESTAMP,score int, edited Boolean,silver int, gold int,platinum int,is_top BOOLEAN,is_submitter BOOLEAN,primary key(CommentID),foreign key(RedditorID) references Redditor(RedditorID) ON DELETE CASCADE ON UPDATE CASCADE,foreign key(SubredditID) references Subreddits(SubredditID) ON DELETE CASCADE ON UPDATE CASCADE,foreign key(PostID) references Posts(PostID) ON DELETE CASCADE ON UPDATE CASCADE)"

    FlairsTableSql = "CREATE TABLE Flairs(RedditorID int,SubredditID int, flair varchar(500), foreign key(RedditorID) references Redditors(RedditorID) ON DELETE CASCADE ON UPDATE CASCADE, foreign key(SubredditID) references Subreddits(SubredditID) ON DELETE CASCADE)"    
    # a list of tables and their sql statements in order to iterate through them easily
    tables = [['Subreddits',SubredditTableSql],['Posts',PostsTableSql],['Redditor',RedditorTableSql],['Comments',CommentsTableSql],['Flairs',FlairsTableSql]]
    
    for table in tables:
        #if the table doesnt already exists create it
        if cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+table[0]+"'").fetchall()==[]:
            print("CREATING TABLE "+table[0])
            cursor.execute(table[1])
RedditDataBaseCreation("RedditDatabase.db")

            
def insertData(dbFileName,values,sqlInsert,sqlReturn,uniqueValue):
    '''
    Inserts a datapoint into a specified table and returns the ID of the
    insertion.
    
    Keyword Arguments:
    
    dbFileName -- the sqlite database file that the database will be stored in
    
    values -- a tuple containing the data that will be inserted. order must be
    the same as the columns in sqlInsert
    
    sqlInsert -- the sql statement for the data insertion
    
    sqlReturn -- the sql statement to get the id of the data inserted using a unique attribute
    
    uniqueValue -- the value of the uniqe attribute from sqlReturn

    Return:
    ID -- the ID of the inserted data
    '''
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    cursor.execute(sqlInsert,values)
    cursor.execute(sqlReturn,(uniqueValue,))
    ID = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return ID

def insertSubreddit(dbFileName,subreddit):
    '''
    inserting a subreddits data into the database
    Keyword Arguments:
    dbFileName -- the sqlite database file that the database will be stored in

    subreddit --  the reddit.subreddit object whose data will be inserted
    Return:
    SubredditID -- The id of the subreddit that was inserted
    '''
    #the attributes that will be stored into the tuple
    subscribers= subreddit.subscribers
    created = datetime.fromtimestamp(subreddit.created)
    name = subreddit.display_name
    description = subreddit.public_description
    title = subreddit.title
    subRedditType =subreddit.subreddit_type
    advertiserCategory = subreddit.advertiser_category
    adultContent = subreddit.over18
    publicTraffic =subreddit.public_traffic
    quarantined = subreddit.quarantine
    spoilersEnabled = subreddit.spoilers_enabled
    restrictPosting = subreddit.restrict_posting
    restrictComments = subreddit.restrict_commenting
    allowImages = subreddit.allow_images
    allowDiscovery = subreddit.allow_discovery
    allowVideogifs = subreddit.allow_videogifs
    allowVideos = subreddit.allow_videos
    OnlyOriginalContent = subreddit.all_original_content
    linksFlairs = subreddit.link_flair_enabled
    userFlairs = subreddit.user_flair_enabled_in_sr
    #all columns in subreddits
    columns = "Subscribers, created ,name ,title ,description  ,subRedditType ,advertiserCategory ,adultContent ,publicTraffic ,quarantined ,spoilersEnabled ,restrictPosting ,restrictComments ,allowImages ,allowDiscovery ,allowVideogifs ,allowVideos ,OnlyOriginalContent,linkFlairs,userFlairs"
    #all the values of each column in the tuple. same order as columns
    values = [subscribers,created,name,title,description,subRedditType,
              advertiserCategory, adultContent, publicTraffic, quarantined, spoilersEnabled,
              restrictPosting, restrictComments, allowImages, allowDiscovery, allowVideogifs,
              allowVideos, OnlyOriginalContent, linksFlairs, userFlairs]
    #insert sql statement
    insertSql = "INSERT INTO Subreddits("+columns+") values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
    #select sql statement to get the subreddit of this tuple
    SelectSql = "SELECT SubredditID FROM Subreddits WHERE name = ?"
    # a call to insertData to actually insert the data
    SubredditID = insertData(dbFileName,values,insertSql,SelectSql,name)
    
    return SubredditID
        
def insertRedditor(dbFileName,redditor):
    '''
    A function to insert a redditor into the Redditor table
    Keyword Arguments:
    
    dbFileName -- the sqlite database file that the database will be stored in

    redditor -- a reddit.redditor object whose data will be stored
    
    Return:
    RedditID -- the id of the redditor tuple that was just inserted
    '''
    name = redditor.name
    isGold = redditor.is_gold
    created = datetime.fromtimestamp(redditor.created_utc)
    
    mod = redditor.is_mod
    link_karma = redditor.link_karma
    comment_karma = redditor.comment_karma
    totalKarma = link_karma + comment_karma
    #some redditors have subreddit objects, some don't so this ensures its set to NULL
    #if it doesn't exist. It is completely random, some do some don't
    bannerImg = "NULL"
    bannerX = "NULL"
    bannerY = "NULL"
    if redditor.subreddit != None:
        description = redditor.subreddit['description']
        if 'banner_size' in redditor.subreddit:
            size = redditor.subreddit['banner_size']
            if redditor.subreddit['banner_size'] != None:
                bannerX = size[0]
                bannerY = size[1]
        over18 = redditor.subreddit['over_18']
        default_icon = redditor.subreddit['is_default_icon']
        default_banner = redditor.subreddit['is_default_banner']
        if redditor.subreddit['banner_img'] != '':
            bannerImg = redditor.subreddit['banner_img']
    else:
        
        description = ''
        over18 = "NULL"
        default_icon = "NULL"
        default_banner = "NULL"

    employee = redditor.is_employee
    verified = redditor.verified
    #all columns in redditor
    columns = "isGold,created,name,description,mod,link_karma,comment_karma,totalKarma,bannerImg,bannerX,bannerY,over18,default_icon,default_banner,employee,verifiedEmail"
    # the values that corresponds to columns
    values = [isGold,created,name,description,mod,link_karma,
              comment_karma,totalKarma,bannerImg,bannerX,bannerY,
              over18,default_icon,default_banner,employee,verified]
    #sql insert statement
    sql = "INSERT INTO Redditor("+columns+") values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    #sql statement to get the ID of the tuple that will be inserted
    selectSql="SELECT RedditorID FROM Redditor WHERE name = ?"
    #call the function that will insert the data and get the id
    RedditID = insertData(dbFileName,values,sql,selectSql,name)
    return RedditID

def insertSubmission(dbFileName,RedditID,SubredditID,post):
    '''
    A function to insert a submission into the database
    Keyword Arguments:
    dbFileName -- the sqlite database file that the database will be stored in

    RedditID -- The ID of the redditor from the database that the post is in

    SubredditID -- The ID of the subreddit from the database that the post is in

    post -- the reddit.Submission object whose data will be stored in

    Return:
    
    PostID -- the ID of the tuple that was inserted
    
    '''
    #attributes that will be stored
    permalink = post.permalink
    score = post.score
    upvoteratio = post.upvote_ratio
    silver = 0
    gold = 0
    platinum = 0
    #some comments are have been awarded some havent, if they havent then
    #post.gildings is a NoneType and will return error therefor it will
    #only search if the post has been awarded
    if bool(post.gilded):
        for key in post.gildings.keys():
            if '1' in key:
                silver = post.gildings[key]
            if '2' in key:
                gold = post.gildings[key]
            if '3' in key:
                platinum = post.gildings[key]
    totalAwards = silver + gold + platinum
    num_crossposts = post.num_crossposts
    num_comment = post.num_comments
    title = post.title 
    created = datetime.fromtimestamp(post.created_utc)
    edited = post.edited
    spoiler = post.spoiler
    stickied = post.stickied
    over_18 = post.over_18
    locked = post.locked
    is_meta = post.is_meta
    is_original_content = post.is_original_content
    #the columns of Posts
    columns = "RedditorID,SubredditID,permalink,score,upvoteratio,silver,gold,platinum,totalAwards,num_crossposts,num_comment,title,created,edited,spoiler,stickied,over_18,locked,is_meta,is_original_content"
    #the values coresponding to each column.
    values =[RedditID,SubredditID,permalink,score,upvoteratio,silver,gold,
              platinum,totalAwards,num_crossposts,num_comment,title,created,
              edited,spoiler,stickied,over_18,locked,is_meta,is_original_content]
    #sql for inserting the tuple into the database
    sql = "INSERT INTO Posts ("+columns+") values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    #sql for selecting the tuple that will be inserted
    selectSql = "SELECT PostID FROM Posts WHERE permalink = ?"
    #calling the function that will actually insert the data
    PostID = insertData(dbFileName,values,sql,selectSql,permalink)
    
    return PostID

def insertComment(dbFileName,PostID,RedditID,SubredditID,comment):
    '''
    Inserting a comment into Comments table
    
    Keyword Arguments:
    
    dbFileName -- the sqlite database file that the database will be stored in

    PostID -- The ID of the Post from the database that the comment is in

    RedditID -- The ID of the redditor from the database that the comment is in

    SubredditID -- The ID of the subreddit from the database that the comment is in

    Return:
    CommentID -- The ID of the comment that was just inserted
    '''
    #the submission that the comment was in
    submission = comment.submission
    #Make the submission sort its comment from the top
    submission.comment_sort = 'top'
    #attributes that will be stored in the database
    text = comment.body
    permalink = comment.permalink
    created = datetime.fromtimestamp(comment.created_utc)
    score = comment.score
    edited = bool(comment.edited)
    silver = 0
    gold = 0
    platinum = 0
    #Some comments have not been given gold,silver or platinum,if this is the
    #case then comment.gildings is a NoneType therefor this is testing for that
    if bool(comment.gilded) :
        for key in comment.gildings.keys():
            if '1' in key:
                silver = comment.gildings[key]
            if '2' in key:
                gold = comment.gildings[key]
            if '3' in key:
                platinum = comment.gildings[key]
    #check if the comment is the top one
    is_top = comment == submission.comments[0]
    is_submitter = comment.is_submitter
    #all values that has been saved
    values = [PostID,SubredditID,RedditID,text,permalink,created,score,edited,silver,gold,platinum,is_top,is_submitter]
    #all columns in Comments, matches the order of values
    columns = "PostID,SubredditID,RedditorID,comment,permalink,created,score,edited,silver,gold,platinum,is_top,is_submitter"
    #sql insert statement
    sql = "INSERT INTO Comments("+columns+") VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
    #sql for selecting the tuple that will be inserted
    selectSql = "SELECT CommentID FROM Comments WHERE permalink = ?"
    #calling the function that will actually insert the data
    CommentID = insertData(dbFileName,values,sql,selectSql,permalink)
    return CommentID

def CheckIfUnique(dbFileName,tableName,valueName,Value):
    '''
    Check if a given tuple is already in the database
    Keyword Arguments:
    dbFileName -- the sqlite database file that the database will be stored in

    tableName -- the table that the user is checking

    valueName -- the name of the value that is being checked

    Value -- the actual value of valueName
    
    Return:
    result -- if the value is in the table or not
    '''
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    cursor.execute("Select * FROM "+tableName+" WHERE "+valueName+"=?",(Value,))
    # if the value is unique then the query will return None
    result = cursor.fetchone()==None
    connection.close()
    return result
def getID(dbFileName,tableName,valueName,Value):
    '''
    Get the ID of the first tuple that satisfies your condition
    Keyword Arguments:
    dbFileName -- the sqlite database file that the database will be stored in

    tableName -- the table that the user is checking

    valueName -- the name of the value that is being checked

    Value -- the actual value of valueName

    Return:
    ID --  the ID of the first result shown
    '''
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    cursor.execute("Select * FROM "+tableName+" WHERE "+valueName+"=?",(Value,))
    ID = cursor.fetchone()[0]
    connection.close()
    return ID
def SubredditDataPopulation(dbFileName,subredditName,commentLimit = 100,SubmissionLimit = 100):
    '''
    Get the data from a particular subreddit, including the amount of comments and
    submissions specified
    Keyword Arguments:
    dbFileName -- the sqlite database file that the database will be stored in

    subredditName -- the string name of the subreddit

    commentLimit -- the maximum number of parent comments that will be stored per submission, actual comments
    may be more depending on the replies to the comment as those are stored too. If None
    is passed then it will store as much comments as possible per submission.Sorted
    by top comments

    SubmissionLimit -- The maximum number of top submissions of the subreddit. If None
    is given then the maximum submissions of a subreddit that reddit will allow will be
    scraped.

    '''
    #The reddit object 
    reddit = praw.Reddit(client_id=Bot.client_id,
                         client_secret=Bot.secret,
                         username=Bot.UserName,
                         password=Bot.Password,
                         user_agent = "A reddit parsing bot so I can do sentiment analysis on different subreddits."
                         )
    #a subreddit object for the subreddit passed
    subreddit = reddit.subreddit(subredditName)
    #Only insert the subreddit into the database if it is unique    
    if CheckIfUnique(dbFileName,"Subreddits","name",subreddit.display_name):
        print("Inserting Subreddit "+subredditName)    
        SubredditID = insertSubreddit(dbFileName,subreddit)
    else:
        print("Getting ID of Subreddit:"+subredditName)
        SubredditID = getID(dbFileName,"Subreddits","name",subreddit.display_name)
    #iterate through the submissions in the subreddit
    for submission in subreddit.top(limit = SubmissionLimit):
        redditor = submission.author
        #some accounts can get suspended and it is not possible to scrape data
        #from them. Also some accounts get deleted and when created they are
        #returned as None
        try:
            if redditor != None and not ('is_suspended' in vars(redditor)):
                #sort the comments by top and limit the amount the user can scrape
                submission.comment_limit = commentLimit
                submission.comment_sort = 'top'
                submission.comments.replace_more(limit=0)
                #insert the author of the submission
                if CheckIfUnique(dbFileName,"Redditor","name",redditor.name):
                    print("Adding New Redditor:"+redditor.name)
                    RedditorID = insertRedditor(dbFileName,redditor)
                else:
                    print("Getting ID of Redditor:"+redditor.name)
                    RedditorID = getID(dbFileName,"Redditor","name",redditor.name)
                #insert the submission itself    
                if CheckIfUnique(dbFileName,"Posts","permalink",submission.permalink):
                    print("inserted Submission:"+submission.permalink)
                    SubmissionID = insertSubmission(dbFileName,RedditorID,SubredditID,submission)
                else:
                    print("getting ID of Submission:"+submission.permalink)
                    SubmissionID = getID(dbFileName,"Posts","permalink",submission.permalink)

                for comment in submission.comments.list():
                    author = comment.author
                    #Some redditors cannot be scraped as parts of their data is missing
                    #or praw wont allow it therefore cancel and skip scraping their data
                    try:
                        if author != None:
                            #insert the redditor who commented
                            if CheckIfUnique(dbFileName,"Redditor","name",author.name):
                                print("Adding New Redditor:"+author.name)
                                AuthorID = insertRedditor(dbFileName,author)
                            else:
                                print("Getting ID of Redditor:"+author.name)
                                AuthorID = getID(dbFileName,"Redditor","name",author.name)
                            #insert the comment they inserted
                            if CheckIfUnique(dbFileName,"Comments","permalink",comment.permalink):
                                print("Inserting comment:"+comment.permalink)
                                insertComment(dbFileName,SubmissionID,AuthorID,SubredditID,comment)
                    except:
                        #show that their data cannot be scraped
                        print("Cannot add comment and redditor:"+author.name)
        except:
            #show that their data cannot be scraped
            print("Cannot add comment and redditor:"+author.name)

def initialDataPopulation(limit,start,end,numComments,numSubmissions,dbFileName):
    '''
    Add new information into the database by looking at the most popular
    subreddits. Growth is not dependent on previous data collection and
    subreddits,comments, posts and redditors who have already been collected
    will not be collected another time.

    Keyword Arguments:
    
    dbFileName -- the sqlite database file that the database will be stored in

    limit --  the number of subreddits the user wants to consider

    start -- the Nth popular subreddit the user wants to start collecting, inclusive

    end -- the Mth poplar subreddit that the user wants to end collecting at, exclusive

    numComments -- the number of comments per submission the user wants to look at.Replies
    will be added as well.

    numSubmissions -- the number of submissions per subreddit the user wants to look at 

    '''
    subreddits = generateListOfSubreddits(limit)[start:end]
    for sub in subreddits:
        print("/////////////////////////////////////////////////////////////////////////////")
        SubredditDataPopulation(dbFileName,sub,numComments,numSubmissions)
           
def growthOfNewSubreddits(dbFileName,new,numComments,numSubmissions):
    '''
    Add new subreddits depending on previous subreddits collected. Should be called
    after initialDaraPopulation is called atleast onetime per database created.

    Keyword Arguments:
    dbFileName -- the sqlite database file that the database will be stored in

    new -- the amount of new subreddits that will be added including the submissions
    and comments specified

    numComments -- the number of parent top comments per submission to be considered.
    Replies will be added as well. 

    numSubmissions -- the number of submissions per subreddit to be considered
    
    '''
    connection = sqlite3.connect(dbFileName)
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(SubredditID) FROM Subreddits")
    start = cursor.fetchone()[0]
    end = start+new
    limit = end+1
    connection.close()
    initialDataPopulation(limit,start,end,numComments,numSubmissions,dbFileName)

def analyzeSubredditPostData(subname):
    '''
    
    '''
    
