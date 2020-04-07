import sys
import csv
import os

csvfile=None
csvOutputDir=None
fitsOutputDir=None
for a in sys.argv[1:]:
    keyvalue=a.split("=")
    if(keyvalue[0]=="--csvfile"):
        csvfile=keyvalue[1]
    if(keyvalue[0]=="--csvout"):
        csvOutputDir=keyvalue[1]
    if(keyvalue[0]=="--fitsout"):
        fitsOutputDir=keyvalue[1]

if csvfile == None:
    print("No CSV file defined")
    exit()

if csvOutputDir == None:
    print("No CSV output directory defined")
    exit()

if csvOutputDir.endswith(os.sep) == False:
    csvOutputDir = csvOutputDir + os.sep

if fitsOutputDir.endswith(os.sep) == False:
    fitsOutputDir = fitsOutputDir + os.sep

if fitsOutputDir == None:
    print("No FITS output directory defined")
    exit()

def getCsvUrl(mjd, plate, fiberID):
    fiberID = fiberID.zfill(4)
    plate = plate.zfill(4)

    return "http://dr12.sdss3.org/csvSpectrum?plateid=" + plate + "&mjd=" + mjd + "&fiber="+fiberID+"&reduction2d=v5_7_0"

def getFitsUrl(mjd, plate, fiberID, run2d, survey):
    fiberID = fiberID.zfill(4)
    plate = plate.zfill(4)
    if survey == "segue2":
        survey = "sdss"

    return "https://dr12.sdss3.org/sas/dr12/" + survey + "/spectro/redux/" + run2d + "/spectra/" + plate + "/spec-" + plate + "-" + mjd + "-"+ fiberID +".fits"

import ssl

import urllib.request
import os.path
def downloadCSVFile(url, target):
    if os.path.exists(target) == True:
        print("Skipping. CSV file has already been downloaded")
        return
    print("Downloading CSV file '" + url + "'...")
    data = None
    with urllib.request.urlopen(url, context=ssl._create_unverified_context()) as response:
        data = response.read()
        response.close()
        print("CSV file downloaded")

    print("Saving CSV file...")
    f = open(target, 'w')
    f.write(data.decode('utf-8'))
    f.close()
    print("CSV file saved")

def downloadFitsFile(url, target):
    if os.path.exists(target) == True:
        print("Skipping. FITS file has already been downloaded")
        return
    print("Downloading fits file '" + url + "'")
    Data = None
    with urllib.request.urlopen(urllib.request.Request(url, data=None, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Upgrade-Insecure-Requests": "1"
    }), context=ssl._create_unverified_context()) as response:
        data = response.read()
        print("Fits file downloaded")

    print("Saving fits file...")
    f = open(target, 'wb')
    f.write(data)
    f.close()
    print("Fits file saved")


with open(csvfile, newline='', ) as csvfile:
    linereader = csv.DictReader(filter(lambda row: row[0]!='#', csvfile))
    for row in linereader:
        rowRes = {}
        for col in row.keys():
            rowRes[col.lower()]=row[col]
        mjd = rowRes["mjd"]
        plate = rowRes["plate"]
        fiberid = rowRes["fiberid"]
        bestobjid = rowRes["bestobjid"]
        run2d = rowRes["run2d"]
        survey = rowRes["survey"]
        print("About to download data for " + bestobjid)

        csvUrl = getCsvUrl(mjd, plate, fiberid)
        downloadCSVFile(csvUrl, csvOutputDir + bestobjid + ".csv")
        fitsUrl = getFitsUrl(mjd, plate, fiberid, run2d, survey)
        downloadFitsFile(fitsUrl, fitsOutputDir + bestobjid + ".fits")