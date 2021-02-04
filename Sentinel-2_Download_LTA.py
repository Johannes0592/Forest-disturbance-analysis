"""
Script to download the Sentinel-2 images from the long time archive,
for the extent of the national park
"""

import sentinelsat
from datetime import date
import logging
import tkinter

# login to scihub
api = sentinelsat.SentinelAPI('johannes0592', 'QthBa9z7x!')
nationalparc = r"F:\Studium_Trier\Masterarbeit\Datensaetze\Geojson\NationalparkGrenzenVereinfacht.json"

#specify boundaries to select images
footprint = sentinelsat.geojson_to_wkt(sentinelsat.read_geojson(nationalparc))
products = api.query(footprint,
                     date=(date(2019, 10, 1), date(2020, 9, 23)),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0,60),
                     processinglevel ='Level-1C',
                     tileid= '32ULA')
                    
                    
ids = []
x = products.keys()
for item in x:
    ids.append(item)
    
# start loop every 30 minutes again to order new images
def downloadLTA():
    global j
    
    print("\n loop started " + str(j) + " time \n")

    # Download from LTA
    for i, item in enumerate(ids):
        product_info = api.get_product_odata(item)
        print(item, i)
        if product_info['Online']:
            print('product {} is online. Starting download.'.format(item))
            api.download(item)
            ids.pop(i)
        else:
            try:
                
                print('product {} is offline'.format(item))
                api.download(item)
            except sentinelsat.SentinelAPILTAError:
                print("SentinelAPILTAError occured.")
    if len(ids) == 0:
        print("all files downloaded")
        return

    tk.after(1850000, downloadLTA)
    j += 1
tk = tkinter.Tk()
j = 0
downloadLTA()
tk.mainloop()
