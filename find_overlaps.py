import csv
import os
from astropy.io import fits

from lib.get_em import get_em

def find_overlaps(csvdir, fitsdir):
    # Infer object ids from the files saved in the csv directory
    object_ids = list(map(lambda d: d.replace(".csv", ""), os.listdir(csvdir)))

    # Gets redshifts from FITS files
    results = {}
    for object_id in object_ids:
        hdulist = fits.open(fitsdir + object_id + ".fits")
        results[object_id] = { "z": hdulist[2].data["Z"][0] }
        hdulist.close()

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

    return {
        "startOverlap": startOverlap,
        "startOverlapZ": startOverlapZ,
        "endOverlap": endOverlap,
        "endOverlapZ": endOverlapZ
    }