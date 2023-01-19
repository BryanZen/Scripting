#!/bin/bash

# Constants; add more if necessary

MISSING_ARGS_MSG="input file and  dictionary missing"
BAD_ARG_MSG_1="missing no. of characters"
BAD_ARG_MSG_2="Third argument must be an integer greater than 0"
FILE_NOT_FOUND_MSG="not a file"

# FILL ME
if [ $# -lt 2 ]; then
    echo "input file and  dictionary missing"
    exit 0
fi
if [ $# -lt 3 ]; then
    echo "$BAD_ARG_MSG_1"
    exit 0
fi 
if [ ! -f $1 ]; then
    echo "$1 $FILE_NOT_FOUND_MSG"
    exit 0
fi 
if [ ! -f $2 ]; then
    echo "$2 $FILE_NOT_FOUND_MSG"
    exit 0
fi
re='^[0-9]+$'
if [ [ $3 -lt 1 ] ] || [ $3 =~ $re ]; then
    echo "$BAD_ARG_MSG_2"
    exit 0
fi 