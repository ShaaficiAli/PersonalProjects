def year_finder(year1,year2,m):
    ''' (int,int,list)--->list

    Finds the amount of books between two years and returns a list of them.
    0(k+log(n)) 
    '''
    yearlist=[]
    if year1>year2:
        year1,year2=year2,year1
    b=0
    e=len(m)-1
    while b<=e:
        mid=(b+e)//2
        if year1==int(m[mid][3][-4:]):
            break
        elif year1<int(m[mid][3][-4:]):
            e=mid-1
        else:
            b=mid+1
        
    upcount=mid
    lowcount=mid-1
    while int(m[upcount][3][-4:])<=year2 :
        if(upcount==1137):
           yearlist+=[m[upcount]]
           break
        yearlist+=[m[upcount]]
        upcount+=1


    while int(m[lowcount][3][-4:])>=year1:
        if(lowcount==0):
            yearlist.insert(0,m[lowcount])
            break
        yearlist.insert(0,m[lowcount])
        lowcount-=1
    return yearlist

def month_finder(month,year,m):
    ''' (int,int,list)--->list
    finds the amount of best sellers within a month
    '''
    monthlist=[]
    for i in range(len(m)):
        if (m[i][3][-7:-5].strip("/")==month and m[i][3][-4:]==year):
            monthlist.append(m[i])
    return monthlist
        
def author_finder(name,m):
    '''
    (string,list)--->list
    Returns the amount of authors that contains the string in their name
    '''
    authorlist=[]
    for i in range(len(m)):
        if(name.lower() in m[i][1].lower()):
            authorlist+=[m[i]]
    return authorlist

def title_finder(name,m):
    '''
    (string,list)-->list
    Returns the amount of titles that contains the string in the list
    '''
    titlelist=[]
    for i in range(len(m)):
        if(name.lower in m[i][0].lower()):
            titlelist+=[m[i][0]]
    return titlelist
def helpfreq(a):
    '''
    (list)--->(list)
    returns a list of the amount of times each unique author name comes up
    '''
     f=[]
     flag=True
     for i in range(len(a)):
          flag=False
          for j in range(len(f)):
               if(a[i][1] == f[j][0]):
                    f[j][1]=f[j][1]+1
                    flag=True
          if(not(flag)):
               f.append([a[i][1],1 ])
     while flag==True:
         flag=False
         for i in range(len(f)-1):
             if f[i][1]>f[i+1][1]:
                 f[i],f[i+1]=f[i+1],f[i]
                 flag=True
     return f
def xbestsellers(x,f):
    '''
    (int,list)-->list
    Returns the amount of authors who has the same or more best sellers than the int given
    '''
    xseller=[]
    for i in range(len(f)):
        if f[i][1]>=x:
            xseller.insert(0,f[i])
    return xseller

def ybestsellers(x,f):
    '''
    (int,list)--->list
    returns the top recurring authors and the length of the list is given by the int
    '''
    if(x>=len(f)):
        return f[-1:-(len(f)):-1]
    yseller=f[-1:-(x+1):-1]
    return yseller

def main_program():
    '''
    (None)--->(None)
    Creates a list of best sellers and uses each of the functiond to give the user information based on what they want.
    '''
    lines = open('bestseller.txt',encoding="utf-8").read().splitlines()
    books=[]
    for line in lines:
        books.append(line.split('\t'))
    for i in range(len(books)):
        books[i][3]=books[i][3].strip()
        books[i][1]=books[i][1].strip()

    flag=True
    while flag==True:
        flag=False
        for i in range(len(books)-1):
            if (int(books[i][3][-4:])>int(books[i+1][3][-4:])):
                books[i],books[i+1]=books[i+1],books[i]
                flag=True

            if (int(books[i][3][-4:])==int(books[i+1][3][-4:])):
                if(int(books[i][3][0:2].strip("/"))>int(books[i+1][3][0:2].strip("/"))):
                    books[i],books[i+1]=books[i+1],books[i]
                    flag=True
                if(int(books[i][3][0:2].strip("/"))==int(books[i+1][3][0:2].strip("/"))):
                    if(int(books[i][3][-7:-5].strip("/"))>int(books[i+1][3][-7:-5].strip("/"))):
                        books[i],books[i+1]=books[i+1],books[i]
                        flag=True
                    
                
            
    f=helpfreq(books)
    flag=True
    while flag==True:    
        print("============================================================")
        print("What would you like to do choose (1,2,3,4,5,6,Q,q)")
        print("1: Look up year range")
        print("2: Look up month/year")
        print("3: Search for author")
        print("4: Search for title")
        print("5: Number of authors with at least x bestsellers")
        print("6: List y authors with the most bestsellers")
        print("============================================================")
        choice=input("Answer(1,2,3,4,5,6,Q,q)")
        while choice not in ["1","2","3","4","5","6","Q","q"]:
            print("Please enter a valid input")
            choice=input("Answer(1,2,3,4,5,6,Q,q):")
        if choice=="1":
            tempflag=True
            while tempflag==True:
                tempflag=False
                try:
                    year1=input("Please enter the first year thats four digits long")
                except:
                    print("enter a valid number")
                    tempflag=True
                if tempflag==False:
                    if float(year1)!=int(year1) or year1<1000 or year1>9999:
                        print("enter a valid number")
                        tempflag=True
            tempflag=True
            while tempflag==True:
                tempflag=False
                try:
                    year2=float(input("Please enter the second year thats four digits long"))
                except:
                    print("enter a valid number")
                    tempflag=True
                if float(year2)!=int(year2) or year2<1000 or year2>9999:
                    print("enter a valid number")
                    tempflag=True
            year_answer=year_finder(int(year1),int(year2),books)
            if (len(year_answer)==0):
                print("There are no books in this time frame")
            else:
                for i in range(len(year_answer)):
                    print(year_answer[i][0]+",","by",year_answer[i][1],"on "+year_answer[i][3])
        if choice =="2":
            tempflag=True
            while tempflag==True:
                tempflag=False
                try:
                    month=input("Enter a number between 1-12:")
                except:
                    print("please enter proper numbers between 1-12:")
                    tempflag=True
                if tempflag==False:
                    if int(month)>12 or int(month)<1 or int(month)!=float(month):
                        print("please enter proper numbers between 1-12:")
                    
            month=int(month)
            tempflag=True
            while tempflag==True:
                tempflag=False
                try:
                    year=float(input("Enter a year"))
                except:
                    print("please enter proper year")
                    tempflag=True
                if tempflag==False:
                    if float(year)!=int(year) or year<1000 or year>9999 :
                        print("Please enter a proper year")
            year=int(year)
            month_answer=month_finder(month,year,books)
            if(len(month_answer)==0):
                print("There are no books in this timeframe")
            else:
                for i in range(month_answer):
                    print(month_answer[i][0]+",","by",month_answer[i][1],"on "+month_answer[i][3])
                
            
        if choice == "3":
            author_search=input("Please enter the authors name:")
            author_answer=author_finder(author_search,books)
            if (len(author_answer)==0):
                print("Sorry we do not have that author here")
            else:
                for i in author_answer:
                    print(i[0].strip("'")+",","by",i[1],i[3])
        if choice =="4":
            title_search=input("Please enter the books name:")
            title_answer=title_finder(title_search,books)
            
            if (len(title_answer)==0):
                print("Sorry we do not have that author here")
            else:
                for i in title_answer:
                    print(i[0].strip("'")+",","by",i[1],i[3])
        if choice =="5":
            tempflag=True
            while tempflag==True:
                tempflag=False
                try:
                    num_authors=input("Please enter a number thats atleast one")
                except:
                    print("enter a valid number")
                    tempflag=True
                
                if int(num_authors)<1 or int(num_authors)!=float(num_authors):
                    print("enter a valid number")
                    tempflag=True
            
            answer_sellers=xbestsellers(num_authors,f)
            print("The number of authors with atleast "+str(num_authors)+" are:")
            for i in range(len(answer_sellers)):
                print((i+1),answer_sellers[i][0]," with",answer_sellers[i][1],"best sellers")
        if choice =="6":
            tempflag=True
            while tempflag==True:
                tempflag=False
                try:
                    y_authors=int(input("Please enter a number thats atleast one"))
                except:
                    print("enter a valid number")
                    tempflag=True
                if y_authors<1 or type(y_authors)!=int:
                    tempflag=True
            answer_y=ybestsellers(y_authors,f)
            print("The top",y_authors,"are:")
            for i in range(len(answer_y)):
                print(str(i+1)+":",answer_y[i][0])
        if choice.lower().strip()=="q":
            print("Thank you for using our services, have a good day")
            break
            
            
main_program()








    
            

    
            
            
    
        








