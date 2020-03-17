import sys
wavelength=None
csvdir=None
fitsdir=None
for a in sys.argv[1:]:
    keyvalue=a.split("=")
    if(keyvalue[0]=="--wavelength"):
        wavelength=float(keyvalue[1])
    if(keyvalue[0]=="--csvdir"):
        csvdir=keyvalue[1]
    if(keyvalue[0]=="--fitsdir"):
        fitsdir=keyvalue[1]
    if(keyvalue[0]=="--output"):
        output=keyvalue[1]


# Infer object ids from the files saved in the csv directory
import os
object_ids=list(map(lambda d:  d.replace(".csv", ""), os.listdir(csvdir)))

# Gets redshifts from FITS files
from astropy.io import fits
results = {}
for object_id in object_ids:
    hdulist = fits.open(fitsdir + object_id + ".fits")
    results[object_id] = {
        "z": hdulist[2].data["Z"][0]
    }
    hdulist.close()

def get_obs(emline, z):
    return emline*(1 + z)

import csv
for object_id in object_ids:
    point_on_continuum=get_obs(wavelength, results[object_id]["z"])
    with open(csvdir + object_id + ".csv", newline='') as csvfile:
        linereader = csv.DictReader(csvfile)
        point_on_continuum_found=False
        results[object_id]["objid"] = object_id
        for line in linereader:
            wlen=float(line["Wavelength"])
            flux=float(line["Flux"])

            if(wlen >= point_on_continuum - 1.0 and wlen <= point_on_continuum + 1.0):
                if(point_on_continuum_found == False or flux > results[object_id]["point_on_continuum"]):
                    results[object_id]["point_on_continuum"] = flux
                point_on_continuum_found=True                

    csvfile.close()

# Find baseline (biggest value)
biggest_point_on_continuum=0
for object_id in object_ids:
    if hasattr(results[object_id], "point_on_continuum") == False:
        print("Error: The object " + object_id + " does not have a point around the wavelength " + str(wavelength))
        exit(1)
    point_on_continuum=results[object_id]["point_on_continuum"]
    if point_on_continuum > biggest_point_on_continuum:
        biggest_point_on_continuum = point_on_continuum

# normalisation values
for object_id in object_ids:
    results[object_id]["normalization"] = biggest_point_on_continuum / results[object_id]["point_on_continuum"]

# print results
if output == None:
    for object_id in object_ids:
        print(results[object_id]["objid"]," z = ", results[object_id]["z"], ",", ": normalization = ", results[object_id]["normalization"])
else:
    file=open(output + "parameters.csv", "w")
    csvwriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    csvwriter.writerow(["#SpecCombine.params"])
    for object_id in object_ids:
        csvwriter.writerow([ int(object_id), results[object_id]["z"], results[object_id]["normalization"] ])
    file.close()
