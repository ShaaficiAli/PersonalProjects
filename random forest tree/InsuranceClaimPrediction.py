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
    '''
    Returns a set with the unique values within a row
    Keyword Arguments:
    rows: The data in row form.
    colNum: the index of the column you want the uniqe values for
    '''
    return set(row[colNum] for row in rows)
def class_counts(rows,classCol):
    '''
    Generates a dictionary of each classtype and the values are the number of occurances.
    Keyword Arguments:
    rows: The data in csv format
    classCol: The column in which the class is named/defined
    '''
    counts = {}
    for row in rows:
        label = row[classCol]
        if label not in counts:
            counts[label] = 0
        counts[label] +=1
    return counts
class Question:
    '''
    A class to help define a node within a decision/random tree. Ex: is your gender M or F.Questions are
    formatted as either is X =< value or is X == value.
    '''
    def __init__(self,column,value,headers):
        '''
        constructor for Question class.
        Keyword Argument:
        column: The column number of the feature that is being questions on. Ex Gender is column 5
        value: what is the feature being compared to.
        headers: list of feautures for each column
        '''
        self.column = column
        self.value = value
        self.headerGiven = headers
    def match(self,row):
        '''
        Function that answers the question and returns result given a datapoint in a boolean.
        Keyword Argument:
        row: the tuple datapoint.
        '''
        val = row[self.column]
        if isinstance(val,float) or isinstance(val,int):
            if(isinstance(val,float) != isinstance(self.value,float)):
                print(self.value)
                print(val)
            return val >= self.value
        else:
            return val == self.value
    def __repr__(self):
        '''
        A string representation of Question class. If the question asks if state == ks it will return "Is state == ks"
        '''
        condition = "=="
        if isinstance(self.value,float) or isinstance(self.value,int):
           condition = ">="
        return "is %s %s %s?"%(self.headerGiven[self.column],condition,str(self.value))
def partition(data, question):
    '''
    Sepearates data depending on question and returns two lists, one in which Question == True and one which Question == False.
    KeyWord Arguments:
    data: the data that is being partitioned
    question: The Question class that will partition the data.
    '''
    true_rows,false_rows = [],[]
    for row in data:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows,false_rows

def giniMeasure(rows):
    '''
    A measure for class purity withing a dataset. Expressed as a probablity of picking the wrong class withing a dataset.Between 1 and 0
    Key word arguments:
    rows: Dataset given
    '''
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
    '''
    A measure of information produced from a random set of data. A measure used within information ratio.
    Keyword arguments:
    rows: Data given
    classCol: The idex value which the class is held in each row
    '''
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
    '''
    Gives the information gain ratio after a split has occured. Measures the quality a split would have if it occured.
    Keyword argument:
    currentPurity: The purity of the class before the split
    OriginalSplit: The Dataset before the split
    splits: a list containg sets of data for after the split
    classCol: The index which the class resides in.
    '''
    
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
    '''
    Finds the best splits for a given dataset that maximizes information Ratio.
    
    Keyword arguments:
    rows: The data given in csv form
    classCol: The index that contains the class name in each header
    headerGiven:The header of teh csv file that has each row name in the order it appears in a datapoint
    '''
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
    '''
    A leaf of a decision tree aka the very bottom node.
    '''
    def __init__(self,data,classCol):
        '''
        The constructor for a leaf object
        Key word arguments:
        data: self explanatory
        classCol: The index for each rpw that the class is on
        '''
        self.predictions = class_counts(data,classCol)
        keys = self.predictions.keys()
        ls = []
        for key in keys:
            ls.append([key,self.predictions[key]])
        ls.sort(key=lambda x:x[1],reverse = True)
        self.mostLikely = ls[0][0]
    def getAllChances(self):
        '''
        Gets the chances for each class to be in the leaf. 
        '''
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
    '''
    A node higher up the decision tree than the leaf. Used to partion the data until pure
    '''
    def __init__(self,question,true_branch,false_branch):
        '''
        A constructor for the decison node.
        Keyword Argument:
        question: A Question class object to partion the data on
        true_branch: The Decision Node/Leaf that is True to the Question
        false_branch: The Decision Node/Leaf that is false to the data
        '''
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
    def __eq__(self,other):
        '''
        an equal function tos ee if two nodes are the same
        Key word Arguments:
        other: Another Decision node object that is being compared.
        '''
        t = self.true_branch == other.true_branch
        f = self.false_branch == other.false_branch
        q = self.question == other.question
        return q and t and f
   # def __hash__(self,other):
        

def buildTree(data,classCol,headers):
    '''
    A recursive function to build the decision tree.
    Keyword arguments:
    data: the data that the decison tree will be based on
    classCol: The index of the column that has the class in it
    headers: The header of the data that has all the features ordered to match the tuples
    '''
    gain,question = findBestSplit(data,classCol,headers)
    if gain < 0.2:
        return Leaf(data,classCol)
    true,false = partition(data,question)
    false_branch = buildTree(false,classCol,headers)
    true_branch = buildTree(true,classCol,headers)
    return Decision_Node(question,true_branch,false_branch)

def print_tree(node,spacing = " "):
    '''
    A function to print a decision tree.
    Keyword argument:
    node: The root of the decision tree
    '''
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
    '''
    A function to classify a datapoint using a decision tree
    KeyWord Argument:
    Node: THe root of the decision tree
    data: The datapoint that is being calssified
    '''
    if isinstance(node,Leaf):
        return node.predictions
    
    if node.question.match(data):
        return classify(node.true_branch, data)
    else:
        return classify(node.false_branch, data)


def sampleFeatures(features,classCol,sampleSize,data):
    '''
    Generates a random subset of features from the features of a dataset and returns a tuple containing the new features and
    a dataset that only contains the new selected features
    Keyword argument:
    features: The full set of features to pick from
    classCol: The index of the column that contains the rows class
    sampleSize: amount of random features you want
    data: The data given
    '''
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
    '''
    Generates a random tree and returns a tuple containing the parent node, features chosen for the random tree and the
    data truncated to match the random features.
    Keyword Arguments:
    data: The data that is used to create the random tree
    features: The list of full features in the proper order
    classCol: The index for the class in each row
    '''
    print(data[:1])
    print(features)
    print(classCol)
    sampleSize = int(math.sqrt(len(features)))
    fixedData,featuresChoosen = sampleFeatures(features,classCol,sampleSize,data)
    randomTree = buildTree(fixedData,len(featuresChoosen) -1,featuresChoosen)
    return (randomTree,featuresChoosen,fixedData)
def trimDatapoint(datapoint,featuresChoosen,originalFeatures,classColOriginal):
    '''
    Trims a datapoint from the original datapoint to one that only contains the features choosen.
    KeyWord Arguments:
    datapoint: the datapoint to be truncated
    featuresChoosen:the features choosen to be in the truncated datapoint
    originalFeatures: the full list of orignial features in the original datapoint
    classColOriginal: The index within the original datapoint taht contains the class
    '''
    newdata = []
    for i in range(len(originalFeatures)):
        if originalFeatures[i] in featuresChoosen:
            if i != classColOriginal:
                newdata.append(datapoint[i])
    newdata.append(datapoint[classColOriginal])
    return newdata
class RandomForest:
    '''
    A RandomForest Object.
    '''
    def __init__(self,listOfTrees,header,listOfFeaturesChoosen,originalFeatureColumn):
        '''
        the constructor for the Random Forest Object
        Keyword Argument:
        listOfTrees: A list containing each random tree in the RandomForest
        header: All the features in order of how they appear in each datapoint
        listOfFeaturesChoosen: An ordered list of random features choosen for randomForest
        originalFeaturesColumn:The index for the column that contains the class for each datapoint
        '''
        self.RF = listOfTrees
        self.h = header
        self.FC = listOfFeaturesChoosen
        self.featureColumn = originalFeatureColumn
        
    def classifyFromRandomForest(self,datapoint):
        '''
        Classifying a datapoint using the random forest.Returns the most likely class for that datapoint
        Keyword Argument:
        datapoint: The datapoint that is being tested.
        '''
        prediction = {}
        results = []
        for i in  range(len(self.RF)):
            dp = trimDatapoint(datapoint,self.FC[i],self.h,self.featureColumn)
            results.append(classify(self.RF[i],dp))
        for result in results:
            for key in result.keys():
                if key in prediction.keys():         
                    prediction[key] += result[key]
                else:
                    prediction[key] = result[key]
        predictors = prediction.keys()
        mostLikely = max(predictors, key = lambda x:prediction[x])
        return mostLikely
    def testAccuracy(self,data):
        '''
        A function that returns the ratio that the random forest guesses the correct class for the datapoint
        Keyword Argument:
        data: the test data to be used.
        '''
        correctRatio = 0
        for datapoint in data:
            mostLikely = self.classifyFromRandomForest(datapoint)
            if(mostLikely == datapoint[self.featureColumn]):
                correctRatio +=1
        correctRatio /= len(data)
        return correctRatio
            
        
def randomTreeToQueue(q,data,features,classCol):
    '''
    Creates a random tree and puts it in a multiproccess queue.
    KeyWord Argument:
    q: The Queue to be placed in
    data: the data that is being used to generate the random tree
    features: The features the data has
    classCol: The index for the class column
    '''
    q.put(randomTree(data,features,classCol))

'''
This is where the random forest is generated using multiproccessing library. Multiple trees are created at the same
time then put together and tested.
'''
if __name__=='__main__':
    q = mp.Queue()
    processes = []
    rf = []
    fc = []
    starttime = time.time()
    for i in range(8):
        randomData = random.choices(data[:6090],k=6090)
        
        p = mp.Process(target = randomTreeToQueue, args = (q,randomData,header,20,))
        processes.append(p)
        p.start()
        
    while len(rf)<8:
        rft = q.get()
        rNode = rft[0]
        featuresChoosen = rft[1]
        print(featuresChoosen)
        rfixedData = rft[2]
        rf.append(rNode)
        fc.append(featuresChoosen)
        
    for p in processes:     
        p.join()
           
    result = RandomForest(rf,header,fc,20)
    print(result.testAccuracy(data[6090:]))
    
