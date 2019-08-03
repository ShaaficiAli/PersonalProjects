import csv
import math
import random
import multiprocessing as mp
import time
with open('Auto_Insurance_Claims_Sample.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    line = 0
    header = csv_reader.__next__()[1:]
    data = []
    for row in csv_reader:
        for i in range(len(row)):
            try:
                row[i]= float(row[i])
            except:
                ''''''
        data.append(row[1:])   


def unique_vals(rows, colNum):
    return set(row[colNum] for row in rows)
def class_counts(rows,classCol):
    counts = {}
    for row in rows:
        label = row[classCol]
        if label not in counts:
            counts[label] = 0
        counts[label] +=1
    return counts
class Question:
    
    def __init__(self,column,value,headers):
        self.column = column
        self.value = value
        self.headerGiven = headers
    def match(self,row):
        val = row[self.column]
        if isinstance(val,float) or isinstance(val,int):
            if(isinstance(val,float) != isinstance(self.value,float)):
                print(self.value)
                print(val)
            return val >= self.value
        else:
            return val == self.value
    def __repr__(self):
        condition = "=="
        if isinstance(self.value,float) or isinstance(self.value,int):
           condition = ">="
        return "is %s %s %s?"%(self.headerGiven[self.column],condition,str(self.value))
def partition(data, question):
    true_rows,false_rows = [],[]
    for row in data:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows,false_rows

def giniMeasure(rows):
    total = len(rows)
    classCounts = class_counts(rows)
    keys = classCounts.keys()
    purity = 0 
    for key in keys:
        proportion = classCounts[key]/total        
        proportion *= proportion
        purity += proportion
    return 1 - purity    
    
    
def EntropyMeasure(rows,classCol):
    total = len(rows)
    classCounts = class_counts(rows,classCol)
    keys = classCounts.keys()
    purity = 0
    for key in keys:
        proportion = classCounts[key]/total
        entropyPerClass =  proportion * math.log(proportion,2)
        purity += entropyPerClass
    return -1 * purity

def InformationRatio(currentPurity,originalSplit,splits,classCol):
    splitsPurity = 0
    informationContent = 0
    total = len(originalSplit)
    for split in splits:
        splitPurity = EntropyMeasure(split,classCol)
        totalSplit = len(split)
        splitsPurity += (totalSplit*splitPurity)/total
        proportion = (totalSplit/total)
        informationContent +=   proportion * math.log(proportion,2)
    informationGain = currentPurity - splitsPurity
    Ratio = informationGain / (-1 * informationContent)
    return Ratio
        
def findBestSplit(rows,classCol,headerGiven):
    bestGain = 0
    bestQuestion = None
    
    currentPurity = EntropyMeasure(rows,classCol)
    Nfeatures = len(random.choice(rows))
    for col in range(Nfeatures):
        if col!=classCol:
            values = unique_vals(rows,col)
            for val in values:
                question = Question(col,val,headerGiven)
                true_rows, false_rows = partition(rows,question)
                splits = [true_rows,false_rows]
                if len(true_rows) != 0 and len(false_rows) != 0:
                    gain = InformationRatio(currentPurity,rows,splits,classCol)           
                    if gain > bestGain:
                        bestGain = gain
                        bestQuestion = question

    return bestGain,bestQuestion

class Leaf:
    def __init__(self,data,classCol):
        self.predictions = class_counts(data,classCol)
        keys = self.predictions.keys()
        ls = []
        for key in keys:
            ls.append([key,self.predictions[key]])
        ls.sort(key=lambda x:x[1],reverse = True)
        self.mostLikely = ls[0][0]
    def getAllChances(self):
        keys = self.predictions.keys()
        values = self.predictions.values()
        total = sum(values)
        ls = []
        for key in keys:
            ls.append([key,self.predictions[key]/total])
        ls.sort(key=lambda x:x[1],reverse = True)
        for item in ls:
            print(item)
    
        
            
class Decision_Node:
    def __init__(self,question,true_branch,false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
    def __eq__(self,other):
        t = self.true_branch == other.true_branch
        f = self.false_branch == other.false_branch
        q = self.question == other.question
        return q and t and f
   # def __hash__(self,other):
        

def buildTree(data,classCol,headers):
    gain,question = findBestSplit(data,classCol,headers)
    if gain < 0.2:
        return Leaf(data,classCol)
    true,false = partition(data,question)
    false_branch = buildTree(false,classCol,headers)
    true_branch = buildTree(true,classCol,headers)
    return Decision_Node(question,true_branch,false_branch)

def print_tree(node,spacing = " "):
    if isinstance(node,Leaf):
        print(spacing + "Predict", node.predictions)
        print(spacing + "Most Likely:"+node.mostLikely)
        return

    print(spacing+str(node.question))
    print(spacing + '---> True:')
    print_tree(node.true_branch,spacing + " ")
    print(spacing+'---> False:')
    print_tree(node.false_branch,spacing + " ")
    
def classify(node,data):
    if isinstance(node,Leaf):
        return node.predictions
    
    if node.question.match(data):
        return classify(node.true_branch, data)
    else:
        return classify(node.false_branch, data)


def sampleFeatures(features,classCol,sampleSize,data):
    classColumnName = features.pop(classCol)
    featuresChoosen = random.sample(features,k=sampleSize)
    features.insert(classCol,classColumnName)
    orderedFeatures = []
    newdataset = []
    flag = True
    for datapoint in data:
        entry = []
        for i in range(len(features)):
            if features[i] in featuresChoosen:
                entry.append(datapoint[i])
                if flag:
                    orderedFeatures.append(features[i])
                    
        flag = False     
        entry.append(datapoint[classCol])
        newdataset.append(entry)
    orderedFeatures.append(classColumnName)
    return newdataset,orderedFeatures
def randomTree(data,features,classCol):
    print(data[:1])
    print(features)
    print(classCol)
    sampleSize = int(math.sqrt(len(features)))
    fixedData,featuresChoosen = sampleFeatures(features,classCol,sampleSize,data)
    randomTree = buildTree(fixedData,len(featuresChoosen) -1,featuresChoosen)
    return (randomTree,featuresChoosen,fixedData)
def trimDatapoint(datapoint,featuresChoosen,originalFeatures,classColOriginal):
    newdata = []
    for i in range(len(originalFeatures)):
        if originalFeatures[i] in featuresChoosen:
            if i != classColOriginal:
                newdata.append(datapoint[i])
    newdata.append(datapoint[classColOriginal])
    return newdata
class RandomForest:
    def __init__(self,listOfTrees):
        self.RF = listOfTrees
        
    def classify(self,data):
        
        for tree in self.RF:
            print(classify(tree,data))
        
def randomTreeToQueue(q,data,features,classCol):
   q.put(randomTree(data,features,classCol))
    

if __name__=='__main__':
    q = mp.Queue()
    processes = []
    starttime = time.time()
    for i in range(8):
        
        p = mp.Process(target = time.sleep, args = (10,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print("it took:"+str(time.time()-starttime))
   
    
    
##    rf = []
##    print("All proccesses have started")
##    while(not(q.empty())):
##        rft = q.get()
##        rNode = rft[0]
##        featuresChoosen = rft[1]
##        print(featuresChoosen)
##        rfixedData = rft[2]
##        rf.append(rNode)
##    print("creating random forest")    
##    result = RandomForest(rf)
##    result.classify(data[-1])
