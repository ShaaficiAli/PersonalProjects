import numpy as np
import statistics as stat
import cv2
import math
import scipy.ndimage
import pickle
from matplotlib import pyplot as plt
import time
def mean_filter(ls):
    """
    a function to calculate the mean of a 1d array.
    This is used by the generic_cilter function
    """
    return sum(ls)/len(ls)
def ROI(image):
    mask = np.zeros(image.shape, dtype=np.float64)
    channel_count = 1
    
    points = np.array([(1200,200),(1200,0),(1400,200),(1400,0)])
    channel_count = 1
    print(image[1200,200])
    cv2.fillConvexPoly(mask, points, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    
    plt.figure(2)
    plt.imshow(mask,interpolation='nearest')
    plt.colorbar()
    plt.show()
    
def process(acc, dn):
    """
    :param acc: The filename and path for the acceptor tiff file
    :param dn: The filename and path for the donor tiff file
    """
    acceptor = cv2.imread(acc, -1) #reading the acceptor img
    donor = cv2.imread(dn,  -1) #reading the donor img
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
    print(type(acceptor))
    acceptor = acceptor.astype(np.float64)
    donor = donor.astype(np.float64)
    for i in range(len(acceptor[0])):
        for j in range(len(acceptor)):
            #subtracting dark current
            acceptor[i][j]-= dark_current1 + 3*dark_current_SD1
            donor[i][j] -= dark_current2 + 3*dark_current_SD2

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
    with open("fret.file","wb") as f:
        pickle.dump(fret,f, pickle.HIGHEST_PROTOCOL)
    return fret
def analyze(image):
    with open(image, "rb") as f:
        processed_image = pickle.load(f)
    plt.imshow(processed_image, interpolation='nearest')
    plt.colorbar()
    plt.show()
    plt.figure(2)
    h = plt.hist(processed_image.flatten(),90)
    plt.show()
    print(h)
    return processed_image
    
                
            
    
    
    
            
          
    
    
    
    
    
    
