#!/bin/bash

# Constants; add more if necessary

MISSING_ARGS_MSG="Score directory missing"
ERR_MSG="not a directory"

# FILL ME
if [ $# -ne 1 ]; then
    echo  $MISSING_ARGS_MSG
    exit 0
elif [ ! -d $1 ]; then
    echo  "$1 $ERR_MSG"
    exit 0
fi
src=$1
for file in $(find $src -type f -regex "^$src\/prob4-score[0-9]+\.txt$")
do
    echo $(awk -F',' 'NR>1 {
        sum = 0; 
        id = $1;
        $1 = "";
        for (i = 1; i <= NF; i++) {
            sum = sum + $i; 
        }
    } END { 
        letter = "";
        if(sum * 2 >= 93 && sum * 2 <= 100)
            letter = "A";
        else if(sum * 2 >= 80 && sum * 2 <= 92)
            letter = "B";
        else if(sum * 2 >= 65 && sum * 2 <= 79)
            letter = "C";
        else if(sum * 2 <= 65)
            letter = "D";
        print id " : " letter
    }' $file)
done