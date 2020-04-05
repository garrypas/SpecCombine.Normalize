#!/bin/bash

count=0
zip=1
cd fits2
rm -rf ./*.zip
for f in ./*; do
    count=$(( $count +1 ))
    mod=$(( $count % 4 ))
    if [ $mod -eq 0 ]
    then
        zip=$(($zip+1))
        count=0
    fi
    zip "./Redshift (2.5-2.7) part ${zip}.zip" "$f"
done
cd ..