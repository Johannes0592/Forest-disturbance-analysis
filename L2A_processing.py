"""
Script to extract downloaded images and to process
them to level 2A product with sen2cor processor
"""

import os
import zipfile
os.chdir("f:/Studium_Trier/Masterarbeit/Datensaetze")

path = r"F:\Studium_Trier\Masterarbeit\Datensaetze\Sentinel2"
output = r"F:\Studium_Trier\Masterarbeit\Datensaetze\atmoCorrected"
images = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".zip")]

for item in images: 
    with zipfile.ZipFile(item, 'r') as zip_ref:
        zip_ref.extractall(output)
        
path = r"F:\Studium_Trier\Masterarbeit\Datensaetze\atmoCorrected"
images = [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".SAFE")]
for f in images:
    os.chdir("f:/Studium_Trier/Masterarbeit/Datensaetze/Sen2Cor-02.08.00-win64")
    cmd = "L2A_Process.bat "+ f + " --resolution 10 --output_dir " + output
    output
    os.system(cmd)
    
