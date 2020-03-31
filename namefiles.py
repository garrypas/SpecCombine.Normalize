# Example: R 1_502 N 19_207 1237665582713536727.fits
import csv
import os
import sys
import re
from shutil import copy2
from lib.specCombineCleanName import cleanForSpecCombine
from lib.get_object_id import get_object_id 

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

vals = {}
with open(parametersFile, newline='') as file:
    csvfile = csv.reader(file, delimiter=',')
    for row in csvfile:
        if(row[0].startswith("#")):
            continue
        object_id = get_object_id(row[0])
        rowRes = {
            "z": round(float(row[1]), nameRounding),
            "normalizationFactor": round(float(row[2]), nameRounding)
        }
        vals[object_id] = rowRes
file.close()

for src in os.listdir(fitsdir):
    object_id = get_object_id(src)
    if (object_id in vals) == False:
        print("File with ID " + object_id + " does not exist in the parameters file")
        continue
    val = vals[object_id]
    dest = src
    if dest.startswith("R ") == False:
        dest = "R " + cleanForSpecCombine(val["z"]) + " N " + cleanForSpecCombine(val["normalizationFactor"]) + " " + dest
    copy2(fitsdir + src, fitsoutdir + dest)