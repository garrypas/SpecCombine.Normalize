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
  --allowOverlapOverride

echo "😊  Done 😊"
echo "parameters.csv file contains normalisation/redshift values"