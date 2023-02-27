#!/bin/bash 
set -e 
in_dir="/p/tmp/fallah/intake/"
out_dir="/p/tmp/fallah/intake/remaped/"
mkdir -p $out_dir
cdo griddes ${in_dir}/diff_CNRM-CM6-1_CNRM-CERFACS_r1i1p1f2_gr.nc > grids
for file in $(ls ${in_dir}*.nc)
do 
   echo $(basename $file)
   files=$(basename $file)
   cdo -O -mulc,86400 -remapbil,grids $file ${out_dir}${files}_remap_mm_day.nc 
done 
