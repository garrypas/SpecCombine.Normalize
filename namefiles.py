# Example: R 1_502 N 19_207 1237665582713536727.fits
import csv
import os
import sys
import re
from shutil import copy2
from lib.specCombineCleanName import cleanForSpecCombine

nameRounding = 2

fitsdir = None
fitsoutdir = None
parametersFile = None
for a in sys.argv[1:]:
    keyvalue = a.split("=")
    parametersFile = keyvalue[1]
    if(keyvalue[0] == "--parameters"):
        parametersFile = keyvalue[1]
    if(keyvalue[0] == "--fitsdir"):
        fitsdir = keyvalue[1]
    if(keyvalue[0] == "--fitsoutdir"):
        fitsoutdir = keyvalue[1]

if fitsdir == None:
    print("fitsdir is not specified")
    exit()
if fitsoutdir == None:
    print("fitsoutdir is not specified")
    exit()
if parametersFile == None:
    print("parameters is not specified")
    exit()

if fitsdir.endswith(os.path.sep) == False:
    fitsdir = fitsdir + os.path.sep
if fitsoutdir.endswith(os.path.sep) == False:
    fitsoutdir = fitsoutdir + os.path.sep

if os.path.exists(fitsoutdir) == False:
    os.mkdir(fitsoutdir)

vals = []
with open(parametersFile, newline='') as file:
    csvfile = csv.reader(file, delimiter=',')
    for row in csvfile:
        if(row[0].startswith("#")):
            continue
        object_id = re.search('([0-9]*$)',row[0]).group(0)
        rowRes = {
            "object_id": object_id,
            "z": round(float(row[1]), nameRounding),
            "normalizationFactor": round(float(row[2]), nameRounding)
        }
        vals.append(rowRes)
file.close()

for val in vals:
    src = fitsdir + cleanForSpecCombine(val["object_id"]) + ".fits"
    dest = fitsoutdir + "R " + cleanForSpecCombine(val["z"]) + " N " + cleanForSpecCombine(val["normalizationFactor"]) + " " + cleanForSpecCombine(val["object_id"]) + ".fits"
    copy2(src, dest)