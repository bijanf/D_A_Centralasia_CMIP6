#!/home/fallah/.conda/envs/INTAKE/bin/python
# A program tocalculate the differences between the hist-nat and historical
# simulations within CMIP6 forpr overCentralAsia
# for other regions please adopt it accordingly
# This program uses the following libraries
import os
cmd="pip install --upgrade xarray zarr gcsfs cftime nc-time-axis"
#os.system(cmd)
print("starting to import")
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
import zarr
import fsspec
import intake
print("finished importing")
ssp="ssp370"
#=========================================
output_dir="/p/tmp/fallah/intake/"+ssp+"/"
cmd="mkdir -p  "+output_dir
os.system(cmd)

# collect the data from api
url = "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
col = intake.open_esm_datastore(url)

cat = col.search(
        activity_id =["ScenarioMIP","CMIP"], # search for historical and hist-nat (detection and attribution)
        variable_id="pr",              # search for precipitation
        table_id="day",               # monthly values
        experiment_id =[ssp,"historical"] 
    )
target = cat.df[cat.df.experiment_id == ssp]
historical = cat.df[cat.df.experiment_id == "historical"]

kk=0
print("starting the loop")
for zstores in target.zstore.values: 
    # check if its historical exists: 
    target2 = target[target.zstore == zstores]
    if (target2.institution_id.values in historical.institution_id.values)and \
    (target2.source_id.values in historical.source_id.values) and \
    (target2.member_id.values in historical.member_id.values) and \
    (target2.grid_label.values in historical.grid_label.values):
        mapper_histnat = fsspec.get_mapper(zstores)
        historical_target = pd.merge(target2, historical,  how='left', left_on=["institution_id",
                                                            "member_id",
                                                            "grid_label",
                                                            "source_id"],
                  right_on = ["institution_id","member_id" ,"grid_label","source_id"]
                 )
        if len(str(historical_target.zstore_y.values[0])) == 3:
            print("continuing-----------------------")
            continue
        mapper_historical = fsspec.get_mapper(historical_target.zstore_y.values[0])
        
        # get the values: 
        ds_historical = xr.open_zarr(mapper_historical, consolidated=True,
                                     decode_times=True)
        ds_histnat    = xr.open_zarr(mapper_histnat, consolidated=True,
                                     decode_times=True)
        # difference of the last 30 years:
        
    
    
#        print(ds_historical.indexes['time'])
#        print(int(str(ds_historical.indexes['time'][-1])[8:10]))
        if int(str(ds_historical.indexes['time'][-1])[8:10]) == 30: 
          ds_historical.sel(time=slice("1971-01-01","2000-12-30")).to_netcdf("temp_historical.nc")
        else:
          ds_historical.sel(time=slice("1971-01-01","2000-12-31")).to_netcdf("temp_historical.nc")
        cmd  ="cdo -O -timmean -yearpctl,99.9 temp_historical.nc -yearmin temp_historical.nc -yearmax temp_historical.nc temp_historical_yearmax.nc"
        os.system(cmd)
        if int(str(ds_histnat.indexes['time'][-1])[8:10]) == 30:
          ds_histnat.sel(time=slice("2070-01-01","2099-12-30")).to_netcdf("temp_"+ssp+".nc")
        else:
          ds_histnat.sel(time=slice("2070-01-01","2099-12-31")).to_netcdf("temp_"+ssp+".nc")
        cmd  ="cdo -O -timmean -yearpctl,99.9 temp_"+ssp+".nc -yearmin temp_"+ssp+".nc -yearmax temp_"+ssp+".nc temp_"+ssp+"_yearmax.nc"
        os.system(cmd)
        cmd = "cdo -sellonlatbox,0,150,0,90 -sub temp_"+ssp+"_yearmax.nc temp_historical_yearmax.nc "+ output_dir+"/diff_"+target2.source_id.values[0]+"_"+\
                      target2.institution_id.values[0]+\
                      "_"+\
                      target2.member_id.values[0]+\
                      "_"+\
                      target2.grid_label.values[0]+"_"+ssp+"_yearpctl_99_9.nc"
        os.system(cmd)

        os.system("rm *.nc")



#        diff = historical_mean - histnat_mean
        # Write to the netcdf files:
#        diff.to_netcdf(output_dir+"/diff_"+target2.source_id.values[0]+"_"+\
#                      target2.institution_id.values[0]+\
#                      "_"+\
#                      target2.member_id.values[0]+\
#                      "_"+\
#                      target2.grid_label.values[0]+".nc")
#        del diff, ds_historical, ds_histnat
        
        print("FINISHED the "+"diff_"+target2.source_id.values[0]+"_"+ target2.institution_id.values[0]+"_"+target2.member_id.values[0]+"_"+ target2.grid_label.values[0]+".nc")

        print("-------------------------------------------------------------------") 
        kk+=1
print("number of simulations processed == "+str(kk))
