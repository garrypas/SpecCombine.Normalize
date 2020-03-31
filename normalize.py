import sys
import os
import csv
import re

from astropy.io import fits
from find_overlaps import find_overlaps
from lib.get_obs import get_obs
from lib.get_em import get_em
from lib.InsensitiveDictReader import InsensitiveDictReader
from lib.get_object_id import get_object_id

csvdir=None
fitsdir=None
output=None
allowOverlapOverride=False
baseline=None

for a in sys.argv[1:]:
    keyvalue=a.split("=")
    if(keyvalue[0]=="--csvdir"):
        csvdir=keyvalue[1]
    if(keyvalue[0]=="--fitsdir"):
        fitsdir=keyvalue[1]
    if(keyvalue[0]=="--output"):
        output=keyvalue[1]
    if(keyvalue[0]=="--allowOverlapOverride"):
        allowOverlapOverride=True
    if(keyvalue[0]=="--baseline"):
        baseline=float(keyvalue[1])

if csvdir.endswith(os.sep) == False:
    csvdir = csvdir + os.sep
if fitsdir.endswith(os.sep) == False:
    fitsdir = fitsdir + os.sep

overlaps = find_overlaps(csvdir, fitsdir)

if allowOverlapOverride == True:
    print("Overlaps start at " + str(overlaps["startOverlap"]) + " and end at " + str(overlaps["endOverlap"]))
    o=input("Enter start overlap (em) (leave blank to keep as-is):")
    if len(o) > 0:
        overlaps["startOverlap"] = float(o)
    e=input("Enter start overlap (em) (leave blank to keep as-is):")
    if len(e) > 0:
        overlaps["endOverlap"] = float(e)

# Infer object ids from the files saved in the csv directory
csvInputs = list(map(lambda filename: {
    "object_id": get_object_id(filename),
    "filename": csvdir + filename + ".csv"
} , list(map(lambda d:  d.replace(".csv", ""), os.listdir(csvdir)))))
# Gets redshifts from FITS files
results = {}
# In case filename is already named correctly
for filename in os.listdir(fitsdir):
    if filename.endswith(".fits") == False:
        continue
    hdulist = fits.open(fitsdir + filename)
    object_id = get_object_id(filename)
    results[object_id] = {
        "z": hdulist[2].data["Z"][0]
    }
    hdulist.close()

for csvInput in csvInputs:
    object_id = csvInput["object_id"]
    csvFilename = csvInput["filename"]
    with open(csvFilename, newline='') as csvfile:
        linereader = InsensitiveDictReader(csvfile)
        results[object_id]["objid"] = object_id
        results[object_id]["fluxtotal"] = 0.0
        results[object_id]["fluxcount"] = 0.0
        results[object_id]["startflux"] = None
        results[object_id]["startObsWavelength"] = None
        for line in linereader:
            wlen_em = get_em(float(line["wavelength"]), overlaps["redshifts"][object_id])
            flux=float(line["flux"])
            if (wlen_em >= overlaps["startOverlap"] and wlen_em <= overlaps["endOverlap"]):

                results[object_id]["fluxcount"] = results[object_id]["fluxcount"] + 1.0
                results[object_id]["fluxtotal"] = results[object_id]["fluxtotal"] + flux
                if results[object_id]["startflux"] == None:
                    results[object_id]["startflux"] = flux
                if results[object_id]["startObsWavelength"] == None:
                    results[object_id]["startObsWavelength"] = float(line["wavelength"])
                results[object_id]["endflux"] = flux
            results[object_id]["startwavelength"] = overlaps["startOverlap"]
            results[object_id]["endwavelength"] = overlaps["endOverlap"]
    csvfile.close()


for csvInput in csvInputs:
    object_id = csvInput["object_id"]
    if results[object_id]["fluxtotal"] == 0:
        print("Unable to normalise " + object_id + ". Maybe there was no overlap, or no flux on the overlap?")
        exit()
    results[object_id]["flux"] = results[object_id]["fluxtotal"] / results[object_id]["fluxcount"]

if baseline == None:
    # Find baseline (biggest value)
    largest=0
    for csvInput in csvInputs:
        object_id = csvInput["object_id"]
        if results[object_id]["flux"] > largest:
            largest = results[object_id]["flux"]

    # normalisation values
    for csvInput in csvInputs:
        object_id = csvInput["object_id"]
        results[object_id]["normalisation"] = largest / results[object_id]["flux"]
else:
    print("baselining to " + str(baseline))
    for csvInput in csvInputs:
        object_id = csvInput["object_id"]
        results[object_id]["normalisation"] = baseline / results[object_id]["flux"]

# print results
for csvInput in csvInputs:
    object_id = csvInput["object_id"]
    print(results[object_id])
file=open(output + "parameters.csv", "w")
csvwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
csvwriter.writerow(["#SpecCombine.params"])

for csvInput in csvInputs:
    object_id = csvInput["object_id"]
    filename = "R " + str(round(results[object_id]["z"], 2)).replace(".", "_", -1) + " N " + str(round(results[object_id]["normalisation"], 2)).replace(".", "_", -1) + " " + object_id
    csvwriter.writerow([ filename, results[object_id]["z"], results[object_id]["normalisation"] ])
file.close()
