#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: getsub.sh <asst>"
    exit 1
fi

export ITEM=$1
export WHERE='/cmshome/tafliovi/at/scheme'
export SUBMITDIR='/courses/websubmit/cscc24w15/submit'


export WHERETO=$WHERE/submissions/$ITEM

rm -rf $WHERETO
mkdir $WHERETO

for utorid in `ls $SUBMITDIR`
do
    rsync -r $SUBMITDIR/$utorid/$ITEM $WHERETO/$utorid
done
