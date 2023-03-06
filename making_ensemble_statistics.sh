#!/bin/bash 
# calculate the ensemble statistics over members of the model and then all the models
set -e
data_dir="/p/tmp/fallah/intake/remaped/"
scenario="ssp126"
out_dir=${data_dir}/${scenario}
mkdir -p $out_dir
#stat="ensmean"
stat="ensstd"
#-----------------------------------
for model in 'ACCESS-CM2' 'ACCESS-ESM1-5' 'AWI-CM-1-1-MR' 'BCC-CSM2-MR' 'BCC-ESM1' 'CAMS-CSM1-0' 'CESM2' 'CESM2-WACCM' 'CMCC-CM2-SR5' 'CMCC-ESM2' 'CNRM-CM6-1' 'CNRM-CM6-1-HR' 'CNRM-ESM2-1' 'CanESM5' 'EC-Earth3' 'EC-Earth3-AerChem' 'EC-Earth3-CC' 'EC-Earth3-Veg' 'EC-Earth3-Veg-LR' 'FGOALS-g3' 'GFDL-CM4' 'GFDL-ESM4' 'GISS-E2-1-G' 'HadGEM3-GC31-LL' 'HadGEM3-GC31-MM' 'IITM-ESM' 'INM-CM4-8' 'INM-CM5-0' 'IPSL-CM5A2-INCA' 'IPSL-CM6A-LR' 'KACE-1-0-G' 'KIOST-ESM' 'MIROC-ES2L' 'MIROC6' 'MPI-ESM-1-2-HAM' 'MPI-ESM1-2-HR' 'MPI-ESM1-2-LR' 'MRI-ESM2-0' 'NESM3' 'NorESM2-LM' 'NorESM2-MM' 'TaiESM1' 'UKESM1-0-LL'
do 
 echo $model
 number=$(ls ${data_dir}/*${model}*${scenario}*99.nc_remap_mm_day.nc | wc -l)
 echo $number
 if [ $number -eq 0 ]
 then 
 continue
 fi 
 if [ $number -gt 1 ] 
 then 
    cdo -O $stat ${data_dir}/*${model}*${scenario}*99.nc_remap_mm_day.nc ${out_dir}/${model}_${scenario}_${stat}.nc
 else
    cp ${data_dir}/*${model}*${scenario}*99.nc_remap_mm_day.nc ${out_dir}/${model}_${scenario}_${stat}.nc
 fi 
 
done

# now make ensemble statistic over all the models: 
cdo -O $stat  ${out_dir}/*_${scenario}_${stat}.nc ${out_dir}/${scenario}_${stat}.nc

