#!/bin/bash 
module load cdo/2.0.5/gnu/10.2
set -e 
#in_dir="/p/tmp/fallah/intake/ssp585/"
in_dir="/p/tmp/fallah/intake/ssp126/"
out_dir="/p/tmp/fallah/intake/remaped/"
mkdir -p $out_dir
cdo griddes /p/tmp/fallah/intake/diff_CNRM-CM6-1_CNRM-CERFACS_r1i1p1f2_gr_yearpctl_99_9.nc > grids
for file in $(ls ${in_dir}*_yearpctl_99_9.nc)
do 
   echo "-----------------------------------------------------------"
   echo $(basename $file)
   files=$(basename $file)
   echo "-----------------------------------------------------------"
   cdo -O -L -mulc,86400 -remapbil,grids $file ${out_dir}${files}_remap_mm_day_yearmax.nc 
done 
