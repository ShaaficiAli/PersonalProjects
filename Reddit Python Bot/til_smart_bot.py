import praw
import random
from mastersorttext import *
bot=praw.Reddit(client_id='maRvwnBwcS6PTA',
                client_secret='HBmMqmLsECo2UxzgM1BSqYG9jeA',
                password='smartsmart',
                user_agent='a learning bot by Shaafici Ali',
                username='til_smart_bot')
print("Logged in")        
def learn():
    authors=[]
    til=[]
    date=[]
    subreddit=bot.subreddit("todayilearned")
    counter=0
    knowledge=store()
    
    for submission in subreddit.stream.submissions():
        words=submission.title
        writer=submission.author
        time=str(datetime.datetime.now().date())
        if words not in knowledge:
            authors+=[str(writer)]
            til+=[str(words)]
            print()
            counter+=1
        if counter>=10:
            break
    update(til)  
def store():
    tilfile=open('bottil.txt','r').read().splitlines()
    return tilfile
    
def update(til):    
    tilfile=open('bottil.txt','a')
    for i in range(len(til)):            
        tilfile.write(til[i]+"\n")
    tilfile.close()
   
def clear():
    '''
    (None)--->None 
    A function that clears all the information learned by the bot
    '''
    tilfile=open('bottil.txt','w')
      
    tilfile.write("")

    tilfile.close()
   

def lengthsort(l):
    if len(l)==0:
        return []
    x=random.choice(l)
    lt,et,gt=[],[],[]
    for i in l:
        if len(x)>len(i):
            lt+=[i]
        elif len(x)<len(i):
            gt+=[i]
        else:
            et+=[i]
    return lengthsort(lt)+et+lengthsort(gt)
    
def alphabeticalsort(l):
    if len(l)==0:
        return []
    x=random.choice(l)
    lt,et,gt=[],[],[]
    for i in l:
        if x.lower()>i.lower():
            lt+=[i]
        elif x.lower()<i.lower():
            gt+=[i]
        else:
            et+=[i]
    return alphabeticalsort(lt)+et+alphabeticalsort(gt)

def mastersort():
    print(text)
    totallist=store()
    limit=len(totallist)
    print(totallist)
    print("This is the limit:"+str(limit))
    choice=input("Please choose an option and maker sure it is smaller than the limit:")
    flag=False
    while flag==False:
        flag=True
        try:
            if "-" in choice:
                choice=choice.split("-")
                newlist=totallist[int(choice[0]):int(choice[1])+1]
            elif "," in choice:
                choice=list(eval(choice))
                newlist=[]
                for i in choice:
                    newlist.append(totallist[i])
            elif "all" in choice:
                newlist=totallist
            
        except:
            print("Please enter a valid option and make sure to be ")
            flag=False
    flag=False
    preview=input("Would you like to see the list of texts to sort?Enter Yes or No:")
    while flag==False:
        flag=True
        if preview.lower().strip() in ["yes","no"]:
            if preview in "yes":
                for i in newlist:
                    print(i)
                    print()
        else:
            print("Enter a valid option")
            preview=input("Would you like to see the list of texts to sort?Enter Yes or No:")
            
        
        
    flag=False
    while flag==False:
        try:
            sortype=str(input("How would you like to sort the data. By length, or alphabetical order:"))
            flag=True
        except:
            flag=False
        if sortype.lower().strip() not in ["length","alphabetical order"]:
            flag=False
            print("Please enter a valid option")
            print()
    else:
        if sortype.lower().strip()=="length":
            return lengthsort(newlist)
        else:
            return alphabeticalsort(newlist)
def bot():
    print(bottext)
    
    flag=True
    while flag==True:
        answer=input("Which would you like to choose E.x(sort,show,learn or quit) ?Answer here:")
        if answer.lower().strip()=='sort':
            l=mastersort()
            response=input("Would you like the information in this order?Yes or No:")
            if response.lower().strip()=='yes':
                update(l)
        elif answer.lower().strip()=='show':
            l=store()
            for i in l:
                print(i)
                print()
        elif answer.lower().strip()=='learn':
            learn()
        elif answer.lower().strip()=='quit':
            flag=False
        else:
            print("Please enter a valid option")
            answer=input("Answer here:")
            
    
    
    
                
        





















