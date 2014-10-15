#!/bin/bash

#batch output to diff folder
DIFF_FOLDER=./diffs
DATA_FOLDER=./data

if [ -d "$DIFF_FOLDER" ];
then
    rm -rf $DIFF_FOLDER
fi

mkdir $DIFF_FOLDER

for file in $DATA_FOLDER/*
do
    python main.py -s ./data/degimas.log -t $file -o $DIFF_FOLDER/$(basename "$file")
done
