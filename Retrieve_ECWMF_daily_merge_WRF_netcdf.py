#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
import calendar
import os
import datetime as datetime                                              
#from cdo import *
#cdo=Cdo()
savepath="../netcdf/" 
server = ECMWFDataServer()

# Set time:

start_date=datetime.date(2013,6,18)
end_date=datetime.date(2013,6,19)

# Restrict area

global_data=True;    

# Boundaries (not necessary when global=True)
boundary_west=-180 # West boundary in degrees -180 to 180
boundary_east=-180 # East boundary in degrees -180 to 180
boundary_south=-90 # South boundary in degrees -180 to 180
boundary_north=90  # North boundary in degrees -180 to 180

if global_data:
    boundarystring= "-90/-180/90/180"
else:
    boundarystring= "%s/%s/%s/%s"%(boundary_south,boundary_west,boundary_north,boundary_east)

#parameters:

param_sfc=[
              172,   # lsm Land/Sea mask
              134,   # sp: Surface Pressure
              151,   # Mean Sea Level Pressure
              129,   # z: geopotential at surface
              165,   # 10u: U wind at 10m
              166,   # 10v: V wind at 10m
              167,   # 2t: Temperature at 2m
              168,   # 2d: Dewpoint temperature at 2m
              235,   # skt: skin temperature
              31,    # ci: Sea Ice cover
              33,    # rsn: Snow Density
              34,    # sst:Sea surface temperature
              141,   # sd: snow depth (m of water equivalent)
              139,   # stl1: soil tempartaure level 1
              170,   # stl2: soil tempartaure level 2
              183,   # stl3: soil tempartaure level 3
              236,   # stl4: soil tempartaure level 4
              39,    # swvl1: Volumetric soil water layer 1
              40,    # swvl2: Volumetric soil water layer 2
              41,    # swvl3: Volumetric soil water layer 3
              42     # swvl4: Volumetric soil water layer 4
              ]
param_pl=[
              129,   #z : Geopotential
              130,   #t: Temperature
              131,   #u: u component of wind (eastward)
              132,   #v: v component of wind (northward)
              133,   #q: specific humidity
              157    #r: relative humidy
              ]


date=start_date

for n in range(int ((end_date - start_date).days)+1):
    date=start_date + datetime.timedelta(days=n)
    yearpath="%s/%s/"%(savepath,date.strftime("%Y"))
    monthpath="%s/%s/%s/"%(savepath,date.strftime("%Y"),date.strftime("%m"))  
    datestr=date.strftime("%Y%m%d") 
# check if output directory year/month exists otherwise create
    if not os.path.isdir(yearpath):
        os.mkdir(yearpath)
    if not os.path.isdir(monthpath):
            os.mkdir(monthpath)

    target_sfc= "%sERA-Interim_sfc_%s.nc"%(monthpath,datestr) 
    target_pl="%sERA-Interim_pl_%s.nc"%(monthpath,datestr) 
    target_wrf="%sERA-Interim_wrfinput_%s.nc"%(monthpath,datestr)
    print("######### ERA-interim  #########")
    print('get surface data for', datestr,' (YYYYMMDD)')
    print("################################")
    server.retrieve({
    'stream'   : 'oper',
    'class'    : 'ei',
    'dataset'  : "interim",   
    'levtype'  : "sfc",
    'expver'   : '0002',
    'repres'   : 'sh', 
    'type'     : "an",
    'resol'    :  'av',
    'grid'     : '0.25/0.25',  
    'area'     : "%s"%(boundarystring),
    'date'     : "%s/to/%s"%(datestr,datestr),
    'time'     : "0000/0600/1200/1800",
    'step'     : '00',
    'param'    : '/'.join(map(str,param_sfc)),
    'format'   : 'netcdf',
    'target'   : "%s"%target_sfc 
   }) 
    print("################################")	
    print('downloaded and saved surface data for', datestr,' (YYYYMMDD)')
    print('to %s'%target_sfc)
    print("################################")
    print("################################")
    print('get pressure level data for', datestr,' (YYYYMMDD)')
    print("################################")
    server.retrieve({
    'stream'   : 'oper',
    'class'    : 'ei',
    'dataset'  : "interim",   
    'levtype'  : "pl",
    'levelist' : "all",
    'expver'   : '0002',
    'repres'   : 'sh', 
    'type'     : "an",
    'resol'    : 'av',
    'grid'     : '0.25/0.25',  
    'area'     : "%s"%(boundarystring),
    'date'     : "%s/to/%s"%(datestr,datestr),
    'time'     : "0000/0600/1200/1800",
    'step'     : '00',
    'param'    : '/'.join(map(str,param_pl)),#
    'format'   : 'netcdf',
    'target'   : "%s"%target_pl 
   }) 
    print("################################")
    print('downloaded and saved pressure level data for', datestr,' (YYYYMMDD)')
    print('to %s'%target_pl)
    print("################################")
    #cdo.merge(input = target_sfc+" "+ target_pl, output = target_wrf)
    os.system("cdo -O merge %s %s %s"%(target_sfc, target_pl, target_wrf))
    os.remove(target_sfc)
    os.remove(target_pl) 
    print("################################")
    print('merged surface and pressure level data to wrf input format for', datestr,' (YYYYMMDD) and deleted downloaded sfc and pl files')
    print('to %s'%target_wrf)
    print("################################")

print("Data downloaded and merged into WRF input format")
