import sys
import csv

# Exmaple query
# SELECT bestobjid,mjd,plate,fiberid from SpecObj
# WHERE BestObjId IN
# (
# '1237657400804442207',
# '1237654601027616844'
# )

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

def getCsvUrl(mjd, plate, fiberID):
    fiberID = fiberID.zfill(4)
    return "http://dr12.sdss3.org/csvSpectrum?plateid=" + plate + "&mjd=" + mjd + "&fiber="+fiberID+"&reduction2d=v5_7_0"

def getFitsUrl(mjd, plate, fiberID):
    fiberID = fiberID.zfill(4)
    return "https://dr12.sdss3.org/sas/dr12/boss/spectro/redux/v5_7_0/spectra/" + plate + "/spec-" + plate + "-" + mjd + "-"+ fiberID +".fits"

import ssl

import urllib.request
def downloadCSVFile(url, target):
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
    
        # csvUrl = getCsvUrl(mjd, plate, fiberid)
        # downloadCSVFile(csvUrl, csvOutputDir + bestobjid + ".csv")
        fitsUrl = getFitsUrl(mjd, plate, fiberid)
        downloadFitsFile(fitsUrl, fitsOutputDir + bestobjid + ".fits")
