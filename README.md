# Overview

## Prerequisites

Requires Python 3 or above
You should have a folder with CSV spectra and another with corresponding FITS files. By convention they should by named by object Id.

## Usage


## Normaliser

It will find the overlapping wavelength range in the set of files you point it to, and generate a parameters.csv file with all of the other spectra normalised to a baseline spectra (the spectra with most intense flux density). This can be imported into SpecCombine.

1. First run setup.sh (setup.bat on Windows) to setup your machine (requires pip3 to be available globally)

2. Run this command against your folders

```
python3 normalize.py \
  --csvdir="../../Project/Activity 4.5.1/csv/" \
  --fitsdir="../../Project/Activity 4.5.1/fits/" \
  --output="./output-folder/"
```

CLI args
```
--csvdir: where your CSV files live
--fitsdir: where your fits files live
--output: where you want the parameters.csv file to be outputed (directory must exist)
```

Now when you import your FITS files in SpecCombine, just follow up by importing the parameters.csv file this script generates and it will fill in all of the normalization and redshift values for you.

## Find overlaps

This finds the overlapping wavelength region of all the files in the folder you point to.

1. First run setup.sh (setup.bat on Windows) to setup your machine (requires pip3 to be available globally)

2. Run this command against your folders

```
python3 find-overlaps.py \
  --csvdir="../../Project/Activity 4.5.1/csv/" \
  --fitsdir="../../Project/Activity 4.5.1/fits/"
```

CLI args
```
--csvdir: where your CSV files live
--fitsdir: where your fits files live
```

Now when you import your FITS files in SpecCombine, just follow up by importing the parameters.csv file this script generates and it will fill in all of the normalization and redshift values for you.
