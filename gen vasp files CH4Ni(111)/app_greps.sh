#!/bin/bash
for dir in ./batch/*_0
do 
    grep 'T' $dir/OSZICAR > greps/"${dir##*/}"
done 
rm greps/*-*
