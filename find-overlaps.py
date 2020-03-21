import sys
from find_overlaps import find_overlaps, get_em

csvdir=None
fitsdir=None
for a in sys.argv[1:]:
    keyvalue = a.split("=")
    if(keyvalue[0] == "--csvdir"):
        csvdir = keyvalue[1]
    if(keyvalue[0] == "--fitsdir"):
        fitsdir = keyvalue[1]

overlaps = find_overlaps(csvdir, fitsdir)

if overlaps["startOverlap"] == None or overlaps["endOverlap"] == None:
    print("No files processed. Are the folders specified correctly? Do they have files?")
    exit()

if overlaps["startOverlap"] >= overlaps["endOverlap"]:
    print("No overlapping regions")
    exit()

print("Overlap (emitted) starts at " + str(get_em(overlaps["startOverlap"], overlaps["startOverlapZ"])) + " and ends at " + str(get_em(overlaps["endOverlap"], overlaps["endOverlapZ"])) )
print("Overlap (observed) starts at " + str(overlaps["startOverlap"]) + " and ends at " + str(overlaps["endOverlap"]) )