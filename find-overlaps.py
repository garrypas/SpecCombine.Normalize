import sys
csvdir=None
fitsdir=None
for a in sys.argv[1:]:
    keyvalue = a.split("=")
    if(keyvalue[0] == "--csvdir"):
        csvdir = keyvalue[1]
    if(keyvalue[0] == "--fitsdir"):
        fitsdir = keyvalue[1]


# Infer object ids from the files saved in the csv directory
import os
object_ids = list(map(lambda d: d.replace(".csv", ""), os.listdir(csvdir)))

# Gets redshifts from FITS files
from astropy.io import fits
results = {}
for object_id in object_ids:
    hdulist = fits.open(fitsdir + object_id + ".fits")
    results[object_id] = { "z": hdulist[2].data["Z"][0] }
    hdulist.close()

def get_em(obs, z):
    return round(obs / (1 + z), 2)

import csv
startOverlap=None
endOverlap=None
startOverlapZ=None
endOverlapZ=None
for object_id in object_ids:
    with open(csvdir + object_id + ".csv", newline='') as csvfile:
        file = []
        for row in csv.DictReader(csvfile):
            file.append(row)
        firstWavelength = round(float(file[0]["Wavelength"]), 2)
        lastWavelength = round(float(file[-1]["Wavelength"]), 2)
        if startOverlap == None or firstWavelength > startOverlap:
            startOverlap = firstWavelength
            startOverlapZ = round(float(results[object_id]["z"]), 2)
        if endOverlap == None or lastWavelength < endOverlap:
            endOverlap = lastWavelength
            endOverlapZ = round(float(results[object_id]["z"]), 2)

    csvfile.close()

if startOverlap == None or endOverlap == None:
    print("No files processed. Are the folders specified correctly? Do they have files?")
    exit()

if startOverlap >= endOverlap:
    print("No overlapping regions")
    exit()

print("Overlap (emitted) starts at " + str(get_em(startOverlap, startOverlapZ)) + " and ends at " + str(get_em(endOverlap, endOverlapZ)) + " (z = " + str(endOverlapZ) +")" )
print("Overlap (observed) starts at " + str(startOverlap) + " and ends at " + str(endOverlap) )