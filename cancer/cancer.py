import numpy as np
import statistics as stat
import cv2
import math
#import matplotlib as plt
import scipy.ndimage
from matplotlib import pyplot as plt

def mean_filter(ls):
    """
    a function to calculate the mean of a 1d array.
    This is used by the generic_cilter function
    """
    return sum(ls)/len(ls)

def analyze(acc, dn):
    """
    :param acc: The filename and path for the acceptor tiff file
    :param dn: The filename and path for the donor tiff file
    """
    acceptor = cv2.imread(acc, cv2.IMREAD_ANYDEPTH) #reading the acceptor img
    donor = cv2.imread(dn,  cv2.IMREAD_ANYDEPTH) #reading the donor img
    #constanst
    dark_current1 = 2000
    dark_current2 = 2000
    dark_current_SD1 = 0
    dark_current_SD2 = 0
    accThresh = 300
    donThresh = 300
    upLimit = 2.0
    lowLimit = 0.0
    limits = [lowLimit, upLimit]
    #number of bins in ir histogram
    num_bin = 90
    binsize = (upLimit-lowLimit)/num_bin
    #percentage data below 
    m0 = 1.35
    m1 = 0.81
    m2 = 0.71
    m4 = 0.6
    #average mask
    acceptor = scipy.ndimage.generic_filter(acceptor, mean_filter, 4)
    donor = scipy.ndimage.generic_filter(donor, mean_filter, 4)
    
    for i in range(len(acceptor[0])):
        for j in range(len(acceptor)):
            #subtracting dark current
            acceptor[i][j]-= dark_current1 + 3*dark_current_SD1
            donor[i][j] -= dark_current2 + 3*dark_current_SD2
            #compensate for the 50_50BS intensity attenuation
            acceptor[i][j] *=1.0
            donor[i][j] *=1.0
            #eliminate low intensity or saturated pixels
            if not(accThresh < acceptor[i][j] < 65000):
                acceptor[i][j] = 0
            if not(donThresh < donor[i][j] < 65000):
                donor[i][j] = 0
    #calculating fret, each pixel is equal to acceptor pixel divide donor pixel
    fret = acceptor
    for i in range(len(fret[0])):
        for j in range(len(fret)):
            #do the division if it is by a non zero else save it as negative one
            if donor[i][j] !=0:
                fret[i][j] = acceptor[i][j]/donor[i][j]
            else:
                fret[i][j] = -1
            #if the pixel is not inbetween the upper and lower limit then set it to 0
            if not(lowLimit <= fret[i][j] <= upLimit):
                fret[i][j] = 0
    
    plt.imshow(fret, interpolation='nearest')
    plt.colorbar()
    plt.show()
    return acceptor
    
                
            
    
    
    
            
          
    
    
    
    
    
    
