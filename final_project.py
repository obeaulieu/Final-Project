#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 21:29:36 2017

@author: livbeaulieu30
"""

# Data organization
# Using a netCDF to organize photos and scan data from DB1

from netCDF4 import Dataset
import numpy as np
from glob import glob
from osgeo import gdal
from numpy import shape

#from PIL import Image
#im=Image.open('Img2.jpg')
#im.size

# create a new netCDF file
file = 'BLcontrolscanFiles.nc'
nc = Dataset(file , 'w' , format='NETCDF4')
#print (nc.file_format)

#data input                                                       

#gtif = gdal.Open( '/Users/livbeaulieu30/Google Drive/Scan Files/*.DAT' )
#print gtif.GetMetadata()
# a = gtif.GetRasterBand(1).ReadAsArray()
datafiles = glob('*.DAT')

ndim = 9450336
xdimension = range(0, 3936)
ydimension = range(0, 2401)
#zdimension = 35
                                                        
#dimensions
#time = nc.createDimension('time', None)
x = nc.createDimension('x', len(xdimension))
y = nc.createDimension('y', len(ydimension))
time = nc.createDimension('time', len(datafiles))
#nc.createDimension('z', zdimension)
                                                        
#variables
x = nc.createVariable('x', 'f4', ('x',))
y = nc.createVariable('y', 'f4', ('y',))
time = nc.createVariable('time', 'f4', ('time',))
#z = nc.createVariable('z', 'f4', ('z',))
nc.createVariable('field', 'f4', ('y', 'x', 'time'))

t_scan = []
i = 0
for datafile in datafiles:
    z1D = np.fromfile(datafile, dtype=np.float32)
    z = np.reshape(z1D, (-1, 3936))
    z[z == -9999] = np.nan # no data handling
    #z = np.flipud(z) # flip top to bottom
    nc.variables['field'][:, :, i] = z
    #plt.imshow(z)
    #plt.show()
    print datafile
    t_scan.append(int(datafile.split('TopoDat_')[1].split('.')[0]))
    i += 1

nc.variables['x'][:] = np.arange(0, len(x)*1E-3, 1E-3)
nc.variables['y'][:] = np.arange(0, len(y)*1E-3, 1E-3)
nc.variables['time'][:] = np.array(t_scan)

x.units = 'Meters'
y.units = 'Meters'


nc.close() 

#import columns of sed flux, water discharge
#import photos, spreadsheets and scans into netcdf
#multiple time dimensions (one for photos, one for scans)
#photos - l,w,RGB,timesteps x, y, 3, t
#get a good naming convention 

#append new data to existing NetCDF
file = 'BLcontrolscanFiles.nc'
nc = Dataset(file , 'a' , format='NETCDF4')

datafiles_p = glob('*.jpg')

npdim = 12212224
xpdimension = range(0, 4288)
ypdimension = range(0, 2848)
rgbdimension = 3
                                                        
#dimensions
#time = nc.createDimension('time', None)
xp = nc.createDimension('xp', len(xpdimension))
yp = nc.createDimension('yp', len(ypdimension))
timep = nc.createDimension('timep', len(datafiles_p))
rgb = nc.createDimension('rgb', 3)
                                                        
#variables
xp = nc.createVariable('xp', 'f4', ('xp',))
yp = nc.createVariable('yp', 'f4', ('yp',))
timep = nc.createVariable('timep', 'f4', ('timep',))
rgb = nc.createVariable('rgb', 'f4', ('rgb',))
nc.createVariable('fieldp', 'f4', ('xp', 'yp', 'rgb', 'timep'))

from PIL import Image
import os
for infile in glob('*.jpg'):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    imgarr = np.array(im)

t_pic = []
i = 0
for datafilep in datafiles_p:
    z1Dp = np.fromfile(datafilep, dtype=np.uint8, count=-1)
    #print(z1Dp.shape)
    #zp = np.reshape(z1Dp, (-1, 4288))
    #zp[zp == -9999] = np.nan # no data handling
    #z = np.flipud(z) # flip top to bottom
    #nc.variables['fieldp'][:, :, i] = zp
    #plt.imshow(z)
    #plt.show()
    print datafilep
    t_pic.append(int(datafilep.split('Img')[1].split('.')[0]))
    i += 1

nc.variables['xp'][:] = np.arange(0, len(xp)*1E-3, 1E-3)
nc.variables['yp'][:] = np.arange(0, len(yp)*1E-3, 1E-3)
nc.variables['rgb'][:] = np.arange(0, 3)
nc.variables['timep'][:] = np.array(t_pic)

xp.units = 'Meters'
yp.units = 'Meters'

nc.close()
