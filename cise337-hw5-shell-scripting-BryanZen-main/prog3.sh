#!/bin/bash

#Constants; add more if necessary
MISSING_ARGS_MSG="Missing data file"

# FILL ME
if [ ! -f $1 ] || [ $# == 0 ]; then
    echo $MISSING_ARGS_MSG
    exit 0
fi
temp=$(awk -F' ' 'END {print NF}' $1)
fields=$((temp - 1))
arr=()
temp2=$fields
while [ $temp2 -gt 0 ]
do
    arr+=(1)
    temp2=$(($temp2-1))
done
weight=0
if [ $# == 1 ]; then 
    weight=$fields    
else
    i=0
    for arg in  ${@:2}; do
        if [ $i -le $(($fields-1)) ]; then
            arr[$i]=$arg
            #weight=$(($weight+$arg))
        fi
        i=$((i+1))
    done
    temp3=0
    while [ $temp3 -le $(($fields-1)) ] 
    do
        weight=$(($weight+${arr[$temp3]}))
        temp3=$((temp3+1))
    done
fi
newarr=($(ps | awk -v a="${arr[*]}" -v weight="$weight" -F' ' 'BEGIN {split(a, A, / /)} NR>1 {for(i=2;i<=NF;i++) sum+=$i * A[i-1]; print sum / weight; sum=0}' $1))
sum=0
size=0
for val in ${newarr[@]}; do
    sum=$(echo $sum + $val | bc)
    size=$((size+1))
done
echo $(echo $sum / $size | bc)