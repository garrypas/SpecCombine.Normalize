mkdir csv
mkdir fits

if [ "$download" != "" ] && [ "$download" != "0" ]
then
    python3 download.py --csvfile=$csvfile --csvout=./csv/ --fitsout=./fits/
fi

python3 normalize.py \
  --csvdir="./csv/" \
  --fitsdir="./fits/" \
  --output="./" \
  --allowOverlapOverride \
  --baseline=100

python3 namefiles.py --fitsdir=./fits --fitsoutdir=./fits2 --parameters=./parameters.csv

bash zip.sh

echo "😊  Done 😊"
echo "parameters.csv file contains normalisation/redshift values. Files are named and added to fits2"