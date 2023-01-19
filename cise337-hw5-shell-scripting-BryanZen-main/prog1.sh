#! /bin/bash

# Contants; add more if necessary
MISSING_ARGS_MSG="src and dest missing"
MORE_ARGS_MSG="Exactly 2 arguments required"
NO_SRC_DIR="src not found"

# FILL ME
if [ $# == 0 ]; then
    echo $MISSING_ARGS_MSG
    exit 0
fi
if [ $# != 2 ]; then
    echo $MORE_ARGS_MSG
    exit 0
fi
if [ ! -d $1 ]; then
    echo $NO_SRC_DIR
    exit 0
fi
if [ -d $2 ]; then
    rm -rf $2
fi
mkdir $2
for x in $(find $1 -type d)
do
    if [[ $(find $x -mindepth 1 -maxdepth 1 -name "*.c" | wc -l) -gt 0 ]]; then
        mkdir -p $2/$x
        if [[ $(find $x -mindepth 1 -maxdepth 1 -name "*.c" | wc -l) -gt 3 ]]; then
            find $x  -mindepth 1 -maxdepth 1 -name "*.c" -print
            read -p "Move files? [y/n] " input
            if [ $input = "y" ] || [ $input = "Y" ]; then
                find $x -mindepth 1 -maxdepth 1 -type f -name "*.c" -exec mv {} $2/$x \;
            fi
        else 
            find $x -mindepth 1 -maxdepth 1 -type f -name "*.c" -exec mv {} $2/$x \;
        fi
    fi
done

rm -rf $2/*.c