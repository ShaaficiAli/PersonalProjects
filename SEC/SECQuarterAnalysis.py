
import os

##Scraping
from bs4 import BeautifulSoup
import requests
import re
import psycopg2
from SECCredentials import SEC_Credentials
import unicodedata


#NLP
import string
import pandas as pd
from gensim.test.utils import get_tmpfile
from gensim.models import Doc2Vec,doc2vec
from gensim.parsing.preprocessing import preprocess_string
import random
import logging
import pickle
def stripReport(report):

    PreReport=bytes.decode(report.tobytes(),errors = "replace")
    reportSoup = BeautifulSoup(PreReport,features="html.parser")
    reportText =  reportSoup.get_text()
    reportText = unicodedata.normalize("NFKD",reportText)
    reportText = preprocess_string(reportText)
    
    return reportText
def buildDoc2Vec():
    
    
    conn = psycopg2.connect(host = SEC_Credentials.host,
                            port = SEC_Credentials.port,
                            user = SEC_Credentials.user,
                            password = SEC_Credentials.password,
                            database = "SECAnalysis")
    curr = conn.cursor(name='formfetch')
    print("Getting formcontent from database")
    curr.execute("SELECT formcontent FROM quarter10 limit 500")
    batch = curr.fetchmany(100)
    reports = batch
    
    counter = 100
    while batch!= []:
        reports.extend(batch)
        batch = curr.fetchmany(100)
        counter+=100
        print("currently inserting batch %s into client side from serverside cursor" %(counter))
    print(curr.rowcount)
    if reports == []:
        return False
   

    
    
    random.shuffle(reports)
    trainingReports = reports[:int(len(reports)*0.8)]
    
    testingReports = [stripReport(report[0]) for report in reports[len(trainingReports):]]
    print("collected and shuffled documents from database")
    #saving the training and tetsing split in pickle
    pickleTrain = []
    
    AllTaggedDocuments = []
    print("Tagging training set documents")
    for i in range(len(trainingReports)):
        print("tagging report:"+str(i))
        currentDoc = stripReport(trainingReports[i][0])
        pickleTrain.append(currentDoc)
        AllTaggedDocuments.append(doc2vec.TaggedDocument(currentDoc,[i]))

    #saving training and testing split for future verification using pickle
    print("Pickling test and training set")    
    with open('trainingSecQuarterSplit.pickle','wb') as trainingfile:
        pickle.dump(pickleTrain,trainingfile)
    with open('testSecQuarterSplit.pickle','wb') as testfile:
        pickle.dump(testingReports,testfile)

    print("Building and training model")
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = doc2vec.Doc2Vec(AllTaggedDocuments,vector_size=300, min_count=2, epochs=10,workers=3)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model.save('SECDOC2VECQuarterReporter.bin')
    conn.close()
    curr.close()



