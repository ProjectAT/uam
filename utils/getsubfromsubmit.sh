#!/bin/bash

export ITEM='lab1'
export WHERE='/cmshome/tafliovi/at/scheme'
export SUBMITDIR='/courses/submit/cscc24w15/submit/'

export WHERETO=$WHERE/submissions/$ITEM


for utorid in `ls $SUBMITDIR`
do
    if [ ! -d $WHERETO/$utorid/$ITEM ]
    then
	rsync -r $SUBMITDIR/$utorid/$ITEM $WHERETO/$utorid
    fi
done



