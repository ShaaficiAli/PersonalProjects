import numpy as np
import pandas as pd
import os
import re

def read_join_csvs(filelist=[]):
    pandaslist = [[re.search("20\d\d",file).group(0),re.search("(5M_20M)|(30K_5M)",file).group(0),pd.read_csv(file, encoding='cp1252')] for file in filelist]
    pandasfixedList=[]
    for dfset in pandaslist:
        df = dfset[-1]
        fiscalyear = dfset[0]
        sizetype = dfset[1]
        print(fiscalyear)
        df['fiscalyear'] = fiscalyear
        df['sizetype'] = sizetype
        
        pandasfixedList.append(df)
    
    df = pd.concat(pandasfixedList)
    return df
def get_files(directory = "."):
    filelist = [file for file in os.listdir(path = directory) if ".csv" in file]
    total_revenue = [file for file in filelist if re.match('Total_revenue',file) !=None]
    Total_expenses_value= [file for file in filelist if re.match('Total_expenses_value',file) !=None]
    Total_expenses_percentage= [file for file in filelist if re.match('Total_expenses_percentage',file) !=None]
    Profit_Non_profit_businesses= [file for file in filelist if re.match('Profit_Non_profit_businesses',file) !=None]
    Profit_Margin_Total_revenue= [file for file in filelist if re.match('Profit_Margin_Total_revenue',file)!=None]
    Profit_Margin_Total_expenses_value= [file for file in filelist if re.match('Profit_Margin_Total_expenses_value',file) !=None]
    Profit_Margin_Total_expenses_percentage= [file for file in filelist if re.match('Profit_Margin_Total_expenses_percentage',file) !=None]
    Profit_Margin_Financial_ratios_Canada_incorporated= [file for file in filelist if re.match('Profit_Margin_Financial_ratios_Canada_incorporated',file) !=None]
    Profit_Margin_Financial_ratios= [file for file in filelist if re.match('Profit_Margin_Financial_ratios',file) !=None and file not in Profit_Margin_Financial_ratios_Canada_incorporated]
    Profit_Margin_Balance_sheet= [file for file in filelist if re.match('Profit_Margin_Balance_sheet',file) !=None]
    Naics_descriptors = [file for file in filelist if re.match('Naics_descriptors',file) !=None]
    Financial_ratios = [file for file in filelist if re.match('Financial_ratios',file)!=None]
    Balance_sheet = [file for file in filelist if re.match('Balance_sheet',file)!=None]
    
    total_revenue = read_join_csvs(filelist = total_revenue)
    Total_expenses_value = read_join_csvs(filelist = Total_expenses_value)
##    Total_expenses_percentage= read_join_csvs(filelist = Total_expenses_percentage)
##    
##    Profit_Non_profit_businesses= read_join_csvs(filelist = Profit_Non_profit_businesses)
##    Profit_Margin_Total_revenue= read_join_csvs(filelist = Profit_Margin_Total_revenue)
##    Profit_Margin_Total_expenses_value= read_join_csvs(filelist = Profit_Margin_Total_expenses_value)
##    Profit_Margin_Total_expenses_percentage= read_join_csvs(filelist = Profit_Margin_Total_expenses_percentage)
##    Profit_Margin_Financial_ratios_Canada_incorporated= read_join_csvs(filelist = Profit_Margin_Financial_ratios_Canada_incorporated)
##    Profit_Margin_Financial_ratios= read_join_csvs(filelist = Profit_Margin_Financial_ratios)
##    Profit_Margin_Balance_sheet= read_join_csvs(filelist = Profit_Margin_Balance_sheet)
##    
    #Naics_descriptors= read_join_csvs(filelist = Naics_descriptors)
##    Financial_ratios= read_join_csvs(filelist = Financial_ratios)
##    Balance_sheet= read_join_csvs(filelist =  Balance_sheet)
    print(total_revenue.columns)
    print(Total_expenses_value.columns)
    finaldf = pd.merge(left = total_revenue,right = Total_expenses_value,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",
       'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on=["Incorporation Status\n\nEtat d'incorporation",'Naics code\n\nCode Scian', 'Province/Canada\n',"fiscalyear","sizetype"])
    print(finaldf.shape)
    return finaldf,Naics_descriptors
    finaldf = pd.merge(left = finaldf,right = Total_expenses_percentage,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\n\nEtat d'incorporation",'Naics code\n\nCode Scian', 'Province/Canada\n',"fiscalyear","sizetype"])
    print(finaldf.dtypes)
    print(finaldf.shape)
    finaldf = pd.merge(left = finaldf,right = Profit_Non_profit_businesses,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatus d'incorporation",'Naics code\nCode Scian', 'Canada\nProvinces',"fiscalyear","sizetype"])


    print(finaldf.shape)
    finaldf = pd.merge(left = finaldf,right = Profit_Margin_Total_revenue,how = "inner",left_on =[ "Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"])

    print(finaldf.shape)
    finaldf = pd.merge(left = finaldf,right = Profit_Margin_Total_expenses_value,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\n\nEtat d'incorporation",'Naics code\n\nCode Scian', 'Province/Canada\n',"fiscalyear","sizetype"])

    print(finaldf.shape)
    finaldf = pd.merge(left = finaldf,right = Profit_Margin_Financial_ratios_Canada_incorporated,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatus d'incorporation",'Naics code\nCode Scian', 'Canada\nProvince',"fiscalyear","sizetype"])


    print(finaldf.shape)
    finaldf = pd.merge(left = finaldf,right =Profit_Margin_Financial_ratios,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatus d'incorporation",'Naics code\nCode Scian', 'Canada\nProvince',"fiscalyear","sizetype"])


    print(finaldf.shape)
    finaldf = pd.merge(left = finaldf,right = Profit_Margin_Balance_sheet,how = "inner",left_on =[ "Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatus d'incorporation",'Naics code\ncode Scian', 'Province\nCanada',"fiscalyear","sizetype"])

    print(finaldf.shape)

    finaldf = pd.merge(left = finaldf,right = Financial_ratios,how = "inner",left_on =[ "Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatus d'incorporation",'Naics code\nCode Scian', 'Canada\nProvince',"fiscalyear","sizetype"])

    print(finaldf.shape)

    finaldf = pd.merge(left = finaldf,right = Balance_sheet,how = "inner",left_on = ["Incorporation Status\nStatue d'incorporation",'Naics_code\nCode_SCIAN', 'Province\nCanada',"fiscalyear","sizetype"],right_on =["Incorporation Status\nStatus d'incorporation",'Naics code\ncode Scian', 'Province\nCanada',"fiscalyear","sizetype"])

    print(finaldf.shape)
    return finaldf,Naics_descriptors
   
    
    

    
         
    
    
    
