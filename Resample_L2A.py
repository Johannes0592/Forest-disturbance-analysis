"""
Script to resample images to given resolution and set extent
"""

import matplotlib.colors as colors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
import numpy as np
import subprocess
import sys
sys.path.append(r'C:\Users\Johannes\Anaconda3\envs\masterarbeit\Lib\snappy')
import snappy
import jpy

# print possible commands of snappy, the SNAP API
print(subprocess.Popen(['gpt', '-h'],stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

# print possible commands for function "subset"
print(subprocess.Popen(['gpt', '-h','Subset'],stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

# print possible commands for function "resample"
print(subprocess.Popen(['gpt', '-h', 'Resample'],stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

# print possible commands for function "write"
print(subprocess.Popen(['gpt', '-h','Write'],stdout=subprocess.PIPE, universal_newlines=True).communicate()[0])

path = r'F:\Studium_Trier\Masterarbeit\Datensaetze\atmoCorrected'
images = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".SAFE")]
print(len(images))

for i, item in enumerate(images):
    # read products
    inputS2 = snappy.ProductIO.readProduct(item)
    
    # resample to 10 m resolution
    params = snappy.HashMap()
    params.put('referenceBand', 'B2')
    params.put('upsampling', 'Nearest')
    resample = snappy.GPF.createProduct('Resample', params, inputS2)
    
    # subset to given bands and extent of NHH
    wkt = "POLYGON ((6.96598264600004 49.5994875390001,6.96598264600004 49.798110884,7.29804284600004 49.798110884,7.29804284600004 49.5994875390001,6.96598264600004 49.5994875390001))"
    bands = "B2,B3,B4,B5,B6,B7,B8,B8A,B11,B12,quality_cloud_confidence,quality_scene_classification"
    parameters = snappy.HashMap()
    parameters.put('copyMetadata', True)
    parameters.put('geoRegion', wkt)
    parameters.put('sourceBands', bands)
    subset = snappy.GPF.createProduct('Subset', parameters, resample)
    
    # write GeoTIFF
    # ToDo: include check if file already exists
    imageName = os.path.basename(item.replace(".SAFE",""))
    folder = r'F:\Studium_Trier\Masterarbeit\Datensaetze\GeoTiffs'
    outPath = os.path.join(folder, imageName + '.tif' )
    if os.path.exists(outPath):
        print(outPath + " already exists.")
    else:
        snappy.ProductIO.writeProduct(subset, outPath, 'GeoTIFF')
        print(outPath + " sucessfully resampled and subseted.")
        
# adapt images to display them with matplotlib
band2 = resample.getBand('B2') # Assign Band to a variable
band3 = resample.getBand('B3')
band4 = resample.getBand('B4')
w = resample.getSceneRasterWidth() # Get Band Width
h = resample.getSceneRasterHeight() # Get Band Height
# Create an empty array
band2_data = np.zeros(w * h, np.float32)
band3_data = np.zeros(w * h, np.float32)
band4_data = np.zeros(w * h, np.float32)
# Populate array with pixel value
band2.readPixels(0, 0, w, h, band2_data)
band3.readPixels(0, 0, w, h, band3_data)
band4.readPixels(0, 0, w, h, band4_data)
# Reshape
band2_data.shape = h, w
band3_data.shape = h, w
band4_data.shape = h, w
rgb = np.ndarray((10980,10980,3),dtype=np.float32)
rgb[:,:,0]=band2_data
rgb[:,:,1]=band3_data
rgb[:,:,2]=band4_data

print(rgb.shape)
print(rgb.dtype)
# Plot the band  
plt.figure(figsize=(18,10))
plt.imshow(rgb)
plt.show()
