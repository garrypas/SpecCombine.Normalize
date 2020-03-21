import sys
import os
import csv

from astropy.io import fits
from find_overlaps import find_overlaps

csvdir=None
fitsdir=None
for a in sys.argv[1:]:
    keyvalue=a.split("=")
    if(keyvalue[0]=="--csvdir"):
        csvdir=keyvalue[1]
    if(keyvalue[0]=="--fitsdir"):
        fitsdir=keyvalue[1]
    if(keyvalue[0]=="--output"):
        output=keyvalue[1]

overlaps = find_overlaps(csvdir, fitsdir)

# Infer object ids from the files saved in the csv directory
object_ids=list(map(lambda d:  d.replace(".csv", ""), os.listdir(csvdir)))

# Gets redshifts from FITS files
results = {}
for object_id in object_ids:
    hdulist = fits.open(fitsdir + object_id + ".fits")
    results[object_id] = {
        "z": hdulist[2].data["Z"][0]
    }
    hdulist.close()

def get_obs(emline, z):
    return emline*(1 + z)

for object_id in object_ids:
    with open(csvdir + object_id + ".csv", newline='') as csvfile:
        linereader = csv.DictReader(csvfile)
        results[object_id]["objid"] = object_id
        results[object_id]["flux"] = 0
        results[object_id]["fluxcount"] = 0
        for line in linereader:
            wlen=float(line["Wavelength"])
            flux=float(line["Flux"])
            if (wlen >= overlaps["startOverlap"] or wlen <= overlaps["endOverlap"]):
                results[object_id]["fluxcount"] = results[object_id]["fluxcount"] + 1
                results[object_id]["flux"] = results[object_id]["flux"] + flux

            results[object_id]["startwavelength"] = overlaps["startOverlap"]
            results[object_id]["endwavelength"] = overlaps["endOverlap"]
    csvfile.close()

for object_id in object_ids:
    if results[object_id]["flux"] == 0:
        print("Unable to normalise " + object_id + ". Maybe there was no overlap, or no flux on the overlap?")
        exit()
    results[object_id]["flux"] = results[object_id]["flux"] / results[object_id]["fluxcount"]

# Find baseline (biggest value)
baseline=0
for object_id in object_ids:
    if results[object_id]["flux"] > baseline:
        baseline = results[object_id]["flux"]

# normalisation values
for object_id in object_ids:
    results[object_id]["normalisation"] = baseline / results[object_id]["flux"]

# print results
for object_id in object_ids:
    print(results[object_id])
file=open(output + "parameters.csv", "w")
csvwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
csvwriter.writerow(["#SpecCombine.params"])
for object_id in object_ids:
    csvwriter.writerow([ int(object_id), results[object_id]["z"], results[object_id]["normalisation"] ])
file.close()
