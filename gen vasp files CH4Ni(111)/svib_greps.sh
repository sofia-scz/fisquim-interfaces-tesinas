#!/bin/bash
for dir in ./nve_batch/*K*
do 
    grep 'T' $dir/OSZICAR > greps/"${dir##*/}"
done 
