import numpy as np
import statistics as stat
import cv2
import math
#import matplotlib as plt
import scipy.ndimage
from matplotlib import pyplot as plt
import time
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
    start = time.time()
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
    end = time.time()
    print(end-start)
