#!/bin/bash
for i in {1..9}
do
    grep 'EK' batch/mode$i/OSZICAR > greps/mode$i
done
