import csv
import os
from astropy.io import fits

from lib.get_em import get_em
from lib.InsensitiveDictReader import InsensitiveDictReader
from lib.get_object_id import get_object_id

def find_overlaps(csvdir, fitsdir):
    # Infer object ids from the files saved in the csv directory
    csvFiles = list(map(lambda d: {
        "filename": d,
        "object_id": get_object_id(d.replace(".csv", ""))
    }, list(map(lambda d: d.replace(".csv", ""), os.listdir(csvdir)))))

    # Gets redshifts from FITS files
    results = {}
    for csvFile in csvFiles:
        filename = csvFile["filename"]
        object_id = csvFile["object_id"]
        hdulist = fits.open(fitsdir + filename + ".fits")
        results[object_id] = { "z": hdulist[2].data["Z"][0] }
        hdulist.close()

    startOverlap=None
    endOverlap=None
    z={}
    for csvFile in csvFiles:
        filename = csvFile["filename"]
        object_id = csvFile["object_id"]
        with open(csvdir + filename + ".csv", newline='') as csvfile:
            file = []
            for row in InsensitiveDictReader(csvfile):
                file.append(row)

            z[object_id] = float(results[object_id]["z"])
            
            firstWavelength = round(float(file[0]["wavelength"]), 2)
            firstWavelength = get_em(firstWavelength, z[object_id])
            lastWavelength = round(float(file[-1]["wavelength"]), 2)
            lastWavelength = get_em(lastWavelength, z[object_id])

            if startOverlap == None or firstWavelength > startOverlap:
                startOverlap = firstWavelength
            if endOverlap == None or lastWavelength < endOverlap:
                endOverlap = lastWavelength

        csvfile.close()

    return {
        "startOverlap": startOverlap,
        "endOverlap": endOverlap,
        "redshifts": z
    }