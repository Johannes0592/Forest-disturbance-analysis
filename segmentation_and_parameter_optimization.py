"""
code adapted from:
Grippa, T., Lennert, M., Beaumont, B., Vanhuysse, S., Stephenne, N., & Wolff, E. (2017). An open-source semi-automated processing chain for urban object-based classification. Remote Sensing, 9(4), 358.

"""
## Import libraries needed for setting parameters of operating system 
import os
import sys

## Import library for temporary files creation 
import tempfile 

## Import Numpy library
import numpy as np

## Import subprocess
import subprocess

## Import multiprocessing
import multiprocessing

## Define path to the 'grass7x.bat' file
grass7bin_win = os.path.abspath('C:\\Program Files\\GRASS GIS 7.8\\grass78.bat')
os.environ['GISBASE'] = 'C:\\Program Files\\GRASS GIS 7.8'
os.environ['PATH'] = 'C:\\Program Files\\GRASS GIS 7.8\\lib;C:\\Program Files\\GRASS GIS 7.8\\bin;C:\\Program Files\\GRASS GIS 7.8\\extrabin' + os.pathsep + os.environ['PATH']
os.environ['PATH'] = 'C:\\Program Files\\GRASS GIS 7.8\\etc;C:\\Program Files\\GRASS GIS 7.8\\etc\\python;C:\Program Files\GRASS GIS 7.8\Python37' + os.pathsep + os.environ['PATH']
os.environ['PATH'] = 'C:\\Program Files\\GRASS GIS 7.8\\Python37;C:\\Users\\Johannes\\AppData\\Roaming\\GRASS7\\addons\\scripts' + os.pathsep + os.environ['PATH']
os.environ['PATH'] = 'C:\\Users\\Johannes\\Anaconda3\\Lib\\site-packages' + os.pathsep + os.environ['PATH']
os.environ['PYTHONLIB'] = 'C:\\Python27'
os.environ['PYTHONPATH'] = 'C:\\Program Files\\GRASS GIS 7.8\\etc\\python'
os.environ['GIS_LOCK'] = '$$'
os.environ['GISRC'] = 'C:\\Users\\Johannes\\AppData\\Roaming\\GRASS7\\rc'
os.environ['GDAL_DATA'] = 'C:\\Program Files\\GRASS GIS 7.8\\share\\gdal'
## Define GRASS-Python environment
sys.path.append(os.path.join(os.environ['GISBASE'],'etc','python'))

## Add the R software directory to the general PATH
os.environ['PATH'] = 'C:\\Program Files\\R\\R-3.6.1\\bin' + os.pathsep + os.environ['PATH']

## Set R software specific environment variables
os.environ['R_HOME'] = 'C:\Program Files\R\R-3.6.1'
os.environ['R_ENVIRON'] = 'C:\Program Files\R\R-3.6.1\etc\x64'
os.environ['R_DOC_DIR'] = 'C:\Program Files\R\R-3.6.1\doc'
os.environ['R_LIBS'] = 'C:\Program Files\R\R-3.6.1\library'

## Display the current defined environment variables
for key in os.environ.keys():
    print("%s = %s \t" % (key,os.environ[key]))

## Define a empty dictionnary for saving user inputs
user={}

## Enter the path to GRASSDATA folder
user["gisdb"] = "F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\GRASS_Processing"

## Enter the name of the location (existing or for a new one)
user["location"] = "NHH_32632"

## Enter the EPSG code for this location 
user["locationepsg"] = "32632"

## Enter the name of the mapset to use for Unsupervised Segmentation Parameter Optimization (USPO) step
user["uspo_mapsetname"] = "TEST_USPO"

## Enter the name of the mapset to use for segmentation step
user["segmentation_mapsetname"] = "TEST_SEGMENT"

## Enter the name of the mapset to use for classification step
user["classification_mapsetname"] = "TEST_CLASSIF"

## Enter the maximum number of processes to run in parallel
user["nb_proc"] = 4

if user["nb_proc"] > multiprocessing.cpu_count():
    print("The requiered number of cores is higher than the amount available. Please fix it")
    
## Import libraries needed to launch GRASS GIS in the jupyter notebook
import grass.script.setup as gsetup

## Import libraries needed to call GRASS using Python
import grass.script as grass

## Automatic creation of GRASSDATA folder
if os.path.exists(user["gisdb"]):
    print("GRASSDATA folder already exists")
else: 
    os.makedirs(user["gisdb"]) 
    print("GRASSDATA folder created in "+user["gisdb"])

## Automatic creation of GRASS location if it doesn't exist
if os.path.exists(os.path.join(user["gisdb"],user["location"])):
    print( "Location "+user["location"]+" already exists" )
else : 
    if sys.platform.startswith('win'):
        grass7bin = grass7bin_win
        startcmd =  ' -c epsg:' + user["locationepsg"] + ' -e ' + os.path.join(user["gisdb"],user["location"])
        p = subprocess.Popen(['C:\\Program Files\\GRASS GIS 7.8\\grass78.bat', '-c', 'epsg:32632','-e', 'F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\GRASS_Processing\\NHH_32632'], shell=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        out, err = p.communicate()
        if p.returncode != 0:
            print( sys.stderr, 'ERROR: %s' % err)
            print( sys.stderr, 'ERROR: Cannot generate location (%s)' % startcmd)
            sys.exit(-1)
        else:
            print('Created location %s' % os.path.join(user["gisdb"],user["location"]))
    else:
        print('This notebook was developed for use with Windows. It seems you are using another OS.')

### Automatic creation of GRASS GIS mapsets

## Import library for file copying 
import shutil

## USPO mapset
mapsetname=user["uspo_mapsetname"]
if os.path.exists(os.path.join(user["gisdb"],user["location"],mapsetname)):
    print( "'"+mapsetname+"' mapset already exists" )
else: 
    os.makedirs(os.path.join(user["gisdb"],user["location"],mapsetname))
    shutil.copy(os.path.join(user["gisdb"],user["location"],'PERMANENT','WIND'),
                os.path.join(user["gisdb"],user["location"],mapsetname,'WIND'))
    print ("'"+mapsetname+"' mapset created in location "+user["gisdb"])

## SEGMENTATION mapset
mapsetname=user["segmentation_mapsetname"]
if os.path.exists(os.path.join(user["gisdb"],user["location"],mapsetname)):
    print( "'"+mapsetname+"' mapset already exists" )
else: 
    os.makedirs(os.path.join(user["gisdb"],user["location"],mapsetname))
    shutil.copy(os.path.join(user["gisdb"],user["location"],'PERMANENT','WIND'),
                os.path.join(user["gisdb"],user["location"],mapsetname,'WIND'))
    print( "'"+mapsetname+"' mapset created in location "+user["gisdb"])

## CLASSIFICATION mapset
mapsetname=user["classification_mapsetname"]
if os.path.exists(os.path.join(user["gisdb"],user["location"],mapsetname)):
    print( "'"+mapsetname+"' mapset already exists" )
else: 
    os.makedirs(os.path.join(user["gisdb"],user["location"],mapsetname))
    shutil.copy(os.path.join(user["gisdb"],user["location"],'PERMANENT','WIND'),
                os.path.join(user["gisdb"],user["location"],mapsetname,'WIND'))
    print( "'"+mapsetname+"' mapset created in location "+user["gisdb"])

## Import library for managing time in python
import time  

## Function "print_processing_time()" compute processing time and print it.
# The argument "begintime" wait for a variable containing the begintime (result of time.time()) of the process for which to compute processing time.
# The argument "printmessage" wait for a string format with information about the process. 
def print_processing_time(begintime, printmessage):    
    endtime=time.time()           
    processtime=endtime-begintime
    remainingtime=processtime

    days=int((remainingtime)/86400)
    remainingtime-=(days*86400)
    hours=int((remainingtime)/3600)
    remainingtime-=(hours*3600)
    minutes=int((remainingtime)/60)
    remainingtime-=(minutes*60)
    seconds=round((remainingtime)%60,1)

    if processtime<60:
        finalprintmessage=str(printmessage)+str(seconds)+" seconds"
    elif processtime<3600:
        finalprintmessage=str(printmessage)+str(minutes)+" minutes and "+str(seconds)+" seconds"
    elif processtime<86400:
        finalprintmessage=str(printmessage)+str(hours)+" hours and "+str(minutes)+" minutes and "+str(seconds)+" seconds"
    elif processtime>=86400:
        finalprintmessage=str(printmessage)+str(days)+" days, "+str(hours)+" hours and "+str(minutes)+" minutes and "+str(seconds)+" seconds"
    
    return finalprintmessage
 
 ## Saving current time for processing time management
begintime_full=time.time()

## Save the name of the mapset in which to import the data
mapsetname='PERMANENT'

## Launch GRASS GIS working session in the mapset
if os.path.exists(os.path.join(user["gisdb"],user["location"],mapsetname)):
    gsetup.init(os.environ['GISBASE'], user["gisdb"], user["location"], mapsetname)
    print( "You are now working in mapset '"+mapsetname+"'")
else: 
    print("'"+mapsetname+"' mapset doesn't exists in "+user["gisdb"])
    
## Saving current time for processing time management
begintime_optical=time.time()

## Import optical imagery and rename band with color name
print ("Importing optical raster imagery at " + time.ctime())

grass.run_command('r.in.gdal', input="F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\GeoTiffs\\cloudFree1\\MSI_NDVI_vis_nir_20200807.tif", output="optical", overwrite=True)
for rast in grass.list_strings("rast"):
    if rast.find("1")!=-1: grass.run_command("g.rename", overwrite=True, rast=(rast,"MSI"))
    elif rast.find("2")!=-1: grass.run_command("g.rename", overwrite=True, rast=(rast,"NDVI"))
    elif rast.find("3")!=-1: grass.run_command("g.rename", overwrite=True, rast=(rast,"opt_blue"))
    elif rast.find("4")!=-1: grass.run_command("g.rename", overwrite=True, rast=(rast,"opt_green"))
    elif rast.find("5")!=-1: grass.run_command("g.rename", overwrite=True, rast=(rast,"opt_red"))
    elif rast.find("6")!=-1: grass.run_command("g.rename", overwrite=True, rast=(rast,"opt_nir"))
        
print_processing_time(begintime_optical ,"Optical imagery has been imported in ")

## Save default computational region to match the full extend of optical imagery
grass.run_command('g.region', flags="s", raster="opt_red@PERMANENT")

## Set the name of the mapset in which to work
mapsetname=user["uspo_mapsetname"]

## Launch GRASS GIS working session in the mapset
if os.path.exists(os.path.join(user["gisdb"],user["location"],mapsetname)):
    gsetup.init(os.environ['GISBASE'], user["gisdb"], user["location"], mapsetname)
    print("You are now working in mapset '"+mapsetname+"'")
else: 
    print("'"+mapsetname+"' mapset doesn't exists in "+user["gisdb"])

## Import shapefile with polygons corresponding to computational region's extension for USPO 
print ("Importing vector data with USPO's regions at " + time.ctime())

grass.run_command('g.region', flags="d")

grass.run_command('v.import', overwrite=True, 
                  input="F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\shapes\\con_forest_subset_51_32632.shp", 
                  output="region_uspo")
 
 ## Create a computional region for each polygon in the 'region_uspo' layer
print("Defining a GRASS region for each polygon at " + time.ctime())

for cat in grass.parse_command('v.db.select', map='region_uspo',  columns='cat', flags='c'):
    condition="cat="+cat
    outputname="region_uspo_"+cat
    regionname="subset_uspo_"+cat
    grass.run_command('v.extract', overwrite=True, quiet=True, 
                      input="region_uspo", type="area", where=condition, output=outputname)
    grass.run_command('g.region', overwrite=True, vector=outputname, save=regionname, align="opt_red@PERMANENT", flags="u")
    grass.run_command('g.remove', type="vector", name=outputname, flags="f")
    

print("Updating imagery group 'optical' with optical rasters at " + time.ctime())

## Remove existing imagery group nammed "optical". This group was created when importing multilayer raster data
grass.run_command("g.remove", type="group", name="optical", flags="f")

## Add each raster which begin with the prefix "opt" into a new imagery group "optical"
for rast in grass.list_strings("rast", pattern="opt", flag="r"):
    grass.run_command("i.group", group="optical", input=rast)
print("Defining a imagery group with raster used for i.segment.uspo at " + time.ctime())

## Remove existing imagery group named "group"
grass.run_command('g.remove', flags="rf", type="group", name="group")
 
## Add all optical imagery in the imagery group
for rast in grass.list_strings("rast", pattern="opt", flag='r'):
    grass.run_command('i.group', group="group", input=rast)
"""
adapt according to used input imagery
"""
## Add NDVI imagery in the imagery group
grass.run_command('i.group', group="group", input="NDVI@PERMANENT")
grass.run_command('i.group', group="group", input="MSI@PERMANENT")

## list files in the group
print(grass.read_command('i.group', group="group", flags="l"))

## Instal r.neighborhoodmatrix if not yet installed
if "r.neighborhoodmatrix" not in grass.parse_command('g.extension', flags="a"):
    grass.run_command('g.extension', extension="r.neighborhoodmatrix")
    print("r.neighborhoodmatrix have been installed on your computer")
else: print("r.neighborhoodmatrix is already installed on your computer" )

## Instal i.segment.hierarchical if not yet installed
if "i.segment.hierarchical" not in grass.parse_command('g.extension', flags="a"):
    grass.run_command('g.extension', extension="i.segment.hierarchical")
    print("i.segment.hierarchical have been installed on your computer")
else: print("i.segment.hierarchical is already installed on your computer" )

## Instal i.segment.uspo if not yet installed
if "i.segment.uspo" not in grass.parse_command('g.extension', flags="a"):
    grass.run_command('g.extension', extension="i.segment.uspo")
    print("i.segment.uspo have been installed on your computer")
else: print("i.segment.uspo is already installed on your computer")

## Define the optimization function name ("sum" or "f")
opti_f="f"

## Define the alpha, only if selected optimization function is "f"
if opti_f=="f":
    alpha=2
else : alpha=""

## Define the csv output file name, according to the optimization function selected
outputcsv="F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\segmentationResults\\tables\\vis_nir\\20200807_bounds_geoObj_minsize5_min"+str(opti_f)+str(alpha)+".csv"

## Defining a list of GRASS GIS' computational regions where i.segment.uspo will optimize the segmentation parameters
regions_uspo=grass.list_strings("region", pattern="subset_uspo_", flag='r')[0]
for region in grass.list_strings("region", pattern="subset_uspo_", flag='r')[1:]:
    regions_uspo+=","+region

## Running i.segment.uspo
print ("Runing i.segment.uspo at " + time.ctime())
begintime_USPO=time.time()

grass.run_command('i.segment.uspo', overwrite=True, group='group', 
                  output=outputcsv, segment_map="best", 
                  regions=regions_uspo, threshold_start="0.01", threshold_stop="0.7", threshold_step="0.01", minsizes="5", 
                  optimization_function=opti_f, f_function_alpha=alpha, memory="2000", processes=4)

## Create a .csvt file containing each colomn type of i.segment.uspo' csv output. Required for further import of .csv file
model_output_desc = outputcsv + "t"
f = open(model_output_desc, 'w')
header_string = '"String","Real","Integer","Real","Real","Real"'
f.write(header_string)
f.close()

## Print
print_processing_time(begintime_USPO, "USPO process achieved in ")

## Define the output folder name, according to the optimization function selected
outputfolder="F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\segmentationResults\\polygons\\vis_nir\\USPO_bestsegment_20200807_bounds_geoObj_minsize5_mín"+str(opti_f)+str(alpha)

## Saving current time for processing time management
print("Begin to export i.segment.uspo results at " + time.ctime())
begintime_exportUSPO=time.time()

count=0
for rast in grass.list_strings("rast", pattern="best_", flag='r'):
    count+=1
    print("Working on raster '"+str(rast)+"' - "+str(count)+"/"+str(len(grass.list_strings("rast", pattern="best_", flag='r'))))
                                                 
    strindex=rast.find("subset_uspo_")
    subregion=rast[strindex: strindex+14]
    vectname="temp_bestsegment_"+subregion
    
    print("Converting raster layer into vector")
    grass.run_command('r.to.vect', overwrite=True, input=rast, output=vectname, type='area')
    
    print("Exporting shapefile")
    grass.run_command('v.out.ogr', overwrite=True, input=vectname, type='area', 
                      output=outputfolder, format='ESRI_Shapefile')
    
    print("Remove newly created vector layer")                                                      
    grass.run_command("g.remove", type="vector", pattern="temp_bestsegment_", flags="rf")
    
## Print
print_processing_time(begintime_exportUSPO, "Export of i.segment.uspo results done in ")

## Set the name of the mapset in which to work
mapsetname=user["segmentation_mapsetname"]

## Launch GRASS GIS working session in the mapset
if os.path.exists(os.path.join(user["gisdb"],user["location"],mapsetname)):
    gsetup.init(os.environ['GISBASE'], user["gisdb"], user["location"], mapsetname)
    print("You are now working in mapset '"+mapsetname+"'")
else: 
    print( "'"+mapsetname+"' mapset doesn't exists in "+user["gisdb"])
    
## Saving current time for processing time management
begintime_segmentation_full=time.time()
grass.run_command('r.in.gdal', input="F:\\Geo_Objekte\\geo_objekte_raster_32632.tif", output="seeds", overwrite=True)

begintime_segmentation=time.time()
## Import Pandas library
import pandas as pd
## Import the optimization results of i.segment.uspo in a dataframe
print("Import .csv file with results of i.segment.uspo on " + time.ctime())
ouaga_uspo=pd.read_csv(outputcsv, sep=',',header=0)
ouaga_uspo.head(3)
## Create temporary dataframe with maximum value of optimization criteria for "USPO's region"
temp=ouaga_uspo.loc[:,['region','optimization_criteria']].groupby('region').max()
temp.head()
## Merge between dataframes for identification of threshold corresponding to the maximum optimizaion criteria of each "USPO's region"
uspo_parameters = pd.merge(ouaga_uspo, temp, on='optimization_criteria').loc[:,['region','threshold','optimization_criteria']].sort_values(by='region')
uspo_parameters.head()
## Save the optimized threshold of each "USPO's region" in a list
uspo_parameters_list=uspo_parameters['threshold'].tolist()


## Save the minimum of optimized threshold in a new variable called "optimized_threshold"
optimized_threshold=round(np.min(uspo_parameters_list),3)
print("The lowest of the 'USPOs region' optimized threshold is "+str(optimized_threshold))

## Import optical imagery and rename band with color name
print ("Importing optical raster imagery at " + time.ctime())


## Copy of imagery group to the current mapset
grass.run_command('g.copy', overwrite=True, group='group@TEST_USPO,group')
print(grass.read_command('i.group', group="group", flags="l"))

    
## Segmentation of current polygon with i.segment
grass.run_command('g.region', overwrite=True, raster="opt_red@PERMANENT")
outputsegment="segmentation_tile_2"
grass.run_command('i.segment', overwrite=True, group="group", output=outputsegment, bounds="seeds", threshold=optimized_threshold, minsize="5", memory="2000")

## Compute processing time and print it
print_processing_time(begintime_segmentation, "Segmentation process on all tiles achieved in ")

## Define the output folder name, according to the optimization function selected
outputfolder="F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\segmentationResults\\segmentation\\vis_nir\\segment_MSI_NDVI20200807_minsize5_min_boundsgeoObj_"+str(opti_f)+str(alpha)
print("Converting raster layer into vector")
grass.run_command('r.to.vect', overwrite=True, input="segmentation_tile_2", output="segment_minsize5_vis_nir_mingeoObj_"+str(opti_f)+str(alpha), type='area')
    
print("Exporting shapefile")
grass.run_command('v.out.ogr', overwrite=True, input="segment_minsize5_vis_nir_mingeoObj_"+str(opti_f)+str(alpha), type='area', output=outputfolder, format='ESRI_Shapefile')

import statistics
statistics.min(uspo_parameters_list)

outputcsv = "F:\\Studium_Trier\\Masterarbeit\\Datensaetze\\segmentationResults\\tables\\msi_ndvi_vis_nir\\20200807_bounds_minsize5_minf2.csv"

ouaga_uspo=pd.read_csv(outputcsv, sep=',',header=0)
ouaga_uspo.head(3)
## Create temporary dataframe with maximum value of optimization criteria for "USPO's region"
temp=ouaga_uspo.loc[:,['region','optimization_criteria']].groupby('region').max()
temp.head()
## Merge between dataframes for identification of threshold corresponding to the maximum optimizaion criteria of each "USPO's region"
uspo_parameters = pd.merge(ouaga_uspo, temp, on='optimization_criteria').loc[:,['region','threshold','optimization_criteria']].sort_values(by='region')
uspo_parameters.head()
## Save the optimized threshold of each "USPO's region" in a list
uspo_parameters_list=uspo_parameters['threshold'].tolist()


## Save the minimum of optimized threshold in a new variable called "optimized_threshold"
optimized_threshold=round(np.median(uspo_parameters_list),3)
optimized_threshold
