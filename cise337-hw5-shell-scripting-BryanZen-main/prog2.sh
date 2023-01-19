#!/bin/bash

# Constants; add more if necessary
WRONG_ARGS_MSG="data file or output file missing"
FILE_NOT_FOUND_MSG="file not found"

# FILL ME
input_file=$1
output_file=$2

if [[ $# -ne 2 ]]; then
    echo $WRONG_ARGS_MSG
    exit 0
fi
if [ ! -f $1 ]; then
    f=$(basename $1)
    echo $f $FILE_NOT_FOUND_MSG
    exit 
fi
if [[ -f $2 ]]; then
    rm -rf $2
    touch $2
elif [[ ! -f $2 ]]; then
    touch $2
fi

awk -F '[;:,]' '{
    for (i=1;i<=NF;i++) sum[i]+=$i;
    } 
        END{
            for (i in sum) print "Col "i" : " sum[i] }' $1>$2