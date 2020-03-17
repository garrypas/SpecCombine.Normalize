# Overview

## Prerequisites

Requires Python 3 or above
You should have a folder with CSV spectra and another with corresponding FITS files. By convention they should by named by object Id.

## Usage

1. First run setup.sh (setup.bat on Windows) to setup your machine (requires pip3 to be available globally)
2. Run this command against your folders

```
python3 normalize.py \
  --wavelength=2000 \
  --csvdir="../../Project/Activity 4.5.1/csv/" \
  --fitsdir="../../Project/Activity 4.5.1/fits/"
```

CLI args
```
--wavelength: the point on the continuum you want to normalise to. In the example above I've selected 2000 Angstrom. Every object must have the wavelength you specify for this to work (mathcing is fuzzy so as long as it has one that is close it should be ok)
--csvdir: where your CSV files live
--fitsdir: where your fits files live
--output: where you want the parameters.csv file to be outputed (directory must exist)
```

Now when you import your FITS files in SpecCombine, just follow up by importing the parameters.csv file this script generates and it will fill in all of the normalization and redshift values for you.
