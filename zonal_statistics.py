"""
Computation of the zonal statistics with arcpy
"""

import arcpy
from arcpy.sa import *
import os

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# compute zonal statistics for each cloud free image and the segmentation (clipped with the con forest layer)
arcpy.env.workspace = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\rfClass"

# Set the local variables
inZoneData = r"F:\Studium_Trier\Masterarbeit\Datensaetze\segmentationResults\segmentation\vis_nir\segment_MSI_NDVI20200807_minsize5_min_boundsgeoObj_f2\segments_conforest_raster_10m_32632.tif"
zoneField = "VALUE"
path=r"F:\Studium_Trier\Masterarbeit\Datensaetze"
bands=["\Band_1","\Band_2","\Band_3","\Band_4","\Band_5","\Band_6","\Band_7","\Band_8","\Band_9","\Band_10"]
images = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".tif")]



# Execute ZonalStatisticsAsTable
for image in images:
    name = os.path.basename(image)[13:19]
    print(name)
    for band in bands:
        outZSaT = ZonalStatisticsAsTable(in_zone_data=inZoneData, zone_field=zoneField, in_value_raster=image+band, 
                                 out_table=name+band[1:]+".dbf", ignore_nodata="NODATA", statistics_type="ALL")
                                 
# new names for columns mean, standard deviation
path=r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\rfClass"
tables = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".dbf")]

for table in tables:
    name = os.path.basename(table)
    print(name)
    arcpy.management.AddFields(
        table, 
        [["M"+name[0:4]+name[-6:-4], 'DOUBLE' ], 
         ["S"+name[0:4]+name[-6:-4], 'DOUBLE']])
    arcpy.CalculateFields_management(table, "PYTHON3", 
                                     [["M"+name[0:4]+name[-6:-4],"!MEAN!"], 
                                      ["S"+name[0:4]+name[-6:-4],"!STD!"]])
    arcpy.DeleteField_management(table, ["MEAN","STD","COUNT","AREA","MAJORITY","MAXIMUM","MEDIAN","MINIMUM","MINORITY",
                                     "RANGE","SUM","VARIETY","MIN","MAX"])

# conversion of dbf tables to csv
arcpy.env.workspace = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\rfClass"
path=r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\rfClass"
tables = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".dbf")]

for table in tables:
    arcpy.TableToTable_conversion(table, path, os.path.splitext(os.path.basename(table))[0]+".csv")

os.path.splitext(os.path.basename(table))[0]

# concatenation of all csv tables and deletion of FID and OID
import pandas as pd
path=r"F:\Studium_Trier\Masterarbeit\Datensaetze"
csvtables = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".csv")]
combined=pd.concat([pd.read_csv(f, delimiter=";") for f in csvtables ],axis=1)
#combined = combined.drop(["OID_","Value"], axis=1)

#convert to csv for later use in R
combined.to_csv(r"F:\Studium_Trier\Masterarbeit\Datensaetze\combinedglcm_20200807.csv", sep=";")

path=r"F:\Studium_Trier\Masterarbeit\Datensaetze"
inTables = r"F:\Studium_Trier\Masterarbeit\Datensaetze\combinedglcm_20200807.csv"
# Execute TableToDBASE
arcpy.TableToDBASE_conversion(inTables, path)

# get dates
path=r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\zonalStatistics"
tables = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".dbf")]
names = [os.path.basename(f)[0:6] for f in tables]
myset = set(names)
namesUnique = list(myset)
namesUnique.sort()
print(namesUnique)

# columns for all dates with NDVI 
table = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\combined.dbf"
for name in namesUnique:
    arcpy.AddField_management(in_table=table, field_name="NDVI"+name, field_type="DOUBLE", field_is_nullable=True)

# columns for all dates with RE2
for name in namesUnique:
    arcpy.AddField_management(in_table=table, field_name="RE2"+name, field_type="DOUBLE", field_is_nullable=True)

# columns for all dates with RE3 
for name in namesUnique:
    arcpy.AddField_management(in_table=table, field_name="RE3"+name, field_type="DOUBLE", field_is_nullable=True)

# columns for all dates with NDMI 
for name in namesUnique:
    arcpy.AddField_management(in_table=table, field_name="NDMI"+name, field_type="DOUBLE", field_is_nullable=True)
    
# NDVI computation for the NDVI fields
table = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\combined.dbf"
for name in namesUnique:
    try:
        arcpy.CalculateField_management(in_table=table, field="NDVI"+name, 
                                    expression='(!M'+name+'7! - !M'+name+'3!) / (!M'+name+'7! + !M'+name+'3!)',
                                    expression_type="PYTHON3")
    except:
        print("error occured")
 
 # NDRE1 computation for the NDRE1 fields
table = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\combined.dbf"
for name in namesUnique:
    try:
        arcpy.CalculateField_management(in_table=table, field="RE2"+name,
                                    expression='(!M'+name+'5! - !M'+name+'4!) / (!M'+name+'5! + !M'+name+'4!)',
                                    expression_type="PYTHON3")
    except:
        print("error occured")
     
# NDRE2 computation for the NDRE2 fields
table = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\combined.dbf"
for name in namesUnique:
    try:
        arcpy.CalculateField_management(in_table=table, field="RE3"+name, 
                                    expression='(!M'+name+'6! - !M'+name+'4!) / (!M'+name+'6! + !M'+name+'4!)',
                                    expression_type="PYTHON3")
    except:
        print("error occured")

# NDMI computation for the NDMI fields
table = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\combined.dbf"
for name in namesUnique:
    try:
        arcpy.CalculateField_management(in_table=table, field="NDMI"+name, 
                                    expression='(!M'+name+'8! - !M'+name+'9!) / (!M'+name+'8! + !M'+name+'9!)',
                                    expression_type="PYTHON3")
    except:
        print("error occured")
 
inTables = r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables\combined.dbf"
arcpy.TableToTable_conversion(inTables, r"F:\Studium_Trier\Masterarbeit\Datensaetze\tables", "VItimeseries.csv")
        
