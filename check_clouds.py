"""
Script to check the subsets for clouds with the quality layers
of the sen2cor processor
"""

import os
import rasterio
import numpy as np
import shutil
import csv

path = r'F:\Studium_Trier\Masterarbeit\Datensaetze\GeoTiffs'
images = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".tif")]

unwantedPixels = dict()

for item in images:
    src = rasterio.open(item)
    classLayer = src.read(12)
    
    # class 3 cloud shadows, class 8 cloud medium prob, class 9 cloud high prob, 
    # class 10 thin cirrus, class 11 snow
    unique, counts = np.unique(classLayer, return_counts = True)
    classCount = dict(zip(unique, counts))
    amountPixels = 0
    
    if classCount.get(3) == None:
        amountPixels = amountPixels + 0
    else:
        amountPixels = amountPixels + classCount.get(3)
        
    if classCount.get(8) == None:
        amountPixels = amountPixels + 0
    else:
        amountPixels = amountPixels + int(classCount.get(8))
        
    if classCount.get(9) == None:
        amountPixels = amountPixels + 0
    else:
        amountPixels = amountPixels + classCount.get(9)
        
    if classCount.get(10) == None:
        amountPixels = amountPixels + 0
    else:
        amountPixels = amountPixels + classCount.get(10) 
        
    if classCount.get(11) == None:
        amountPixels = amountPixels + 0
    else:
        amountPixels = amountPixels + classCount.get(11)
    print(amountPixels)
                
    percentage = float(amountPixels)/float(classLayer.shape[0]*classLayer.shape[1])
    print(percentage)
    unwantedPixels[item]=percentage
    
 # filter for clouds less than 1 %
 
cloudFree = []
for item in unwantedPixels:
    print(item)
    if unwantedPixels[item] < 0.01:
        cloudFree.append(item)
        
# copy cloud free images to own folder

        
