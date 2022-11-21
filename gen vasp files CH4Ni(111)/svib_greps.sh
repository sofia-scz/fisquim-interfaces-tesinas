#!/bin/bash
for dir in ./batch/*K*
do 
    grep 'T' $dir/OSZICAR > greps/"${dir##*/}"
done 
