# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 15:53:11 2015

@author: QCSE-adm
"""

import numpy as np
import matplotlib.pyplot as plt
import libtiff
#from scipy.ndimage.filters import gaussian_filter1d
#from scipy.optimize import curve_fit

scan = 5
displacement =50

f='E:/ND/take2 original polarity/0V 004.tif'
mov = libtiff.TiffFile(f)
movie = mov.get_tiff_array()
movie = np.array(movie[:,:,:],dtype='d')

c1='E:/ND/c1.tif'
mov = libtiff.TiffFile(c1)
c1 = mov.get_tiff_array()
c1 = np.mean(c1[0,50:,:],dtype='d', axis=0)-np.mean(c1[0,0:2,:],dtype='d', axis=0)

c2='E:/ND/c2.tif'
mov = libtiff.TiffFile(c2)
c2 = mov.get_tiff_array()
c2 = np.mean(c2[0,50:,:],dtype='d', axis=0)-np.mean(c2[0,0:2,:],dtype='d', axis=0)

c3='E:/ND/c3.tif'
mov = libtiff.TiffFile(c3)
c3 = mov.get_tiff_array()
c3 = np.mean(c3[0,50:,:],dtype='d', axis=0)-np.mean(c3[0,0:2,:],dtype='d', axis=0)

lamp='E:/ND/lamp.tif'
mov = libtiff.TiffFile(lamp)
lamp = mov.get_tiff_array()
lamp = np.mean(lamp[0,50:,:],dtype='d', axis=0)-np.mean(lamp[0,0:2,:],dtype='d', axis=0)

frame=len(movie[:,0,0])
row=len(movie[0,:,0])
col=len(movie[0,0,:])

movie = np.mean(movie[:,:,:], axis=0)

'''
fig, ax = plt.subplots()
ax.plot(np.arange(0,512,1), c1, label='600/40')
ax.plot(np.arange(0,512,1), c2, label='700LP')
ax.plot(np.arange(0,512,1), c3, label='590/80')
ax.plot(np.arange(0,512,1), lamp, label='lamp')
ax.set_ylabel('Intensity (a.u.)')
ax.set_xlabel('pixel')
ax.set_xlim(0,col)
plt.legend(loc=2, frameon='None')
'''

c1d = np.diff(c1/lamp)
c2d = np.diff(c2/lamp)
c3d = np.diff(c3/lamp)

def movingaverage(interval, window_size):
        window = np.ones(int(window_size))/float(window_size)
        return np.convolve(interval, window, 'same')
        
window_size=10
c1ds = movingaverage(c1d, window_size)
c2ds = movingaverage(c2d, window_size)
c3ds = movingaverage(c3d, window_size)
slope_max = np.zeros(5)
slope_max[0] = int(*np.where(c1ds == c1ds.max()))
slope_max[1] = int(*np.where(c1ds == c1ds.min()))
slope_max[2] = int(*np.where(c2ds == c2ds.max()))
slope_max[3] = int(*np.where(c3ds == c3ds.max()))
slope_max[4] = int(*np.where(c3ds == c3ds.min()))

lambda_fit = np.polyfit(slope_max, np.array([580,620,700,550,630]), 5)
p = np.polyval(lambda_fit, np.arange(0,512,1))

fig, ax = plt.subplots(3, sharex=True)
ax[0].plot(np.arange(0,512,1), c1/lamp*100, label='600/40')
ax[0].plot(np.arange(0,512,1), c2/lamp*100, label='700LP')
ax[0].plot(np.arange(0,512,1), c3/lamp*100, label='590/80')
ax[1].plot(np.arange(0.5,511.5,1), c1d, label='600/40d', marker='o', markersize=1)
ax[1].plot(np.arange(0.5,511.5,1), c2d, label='700LPd',  marker='o', markersize=1)
ax[1].plot(np.arange(0.5,511.5,1), c3d, label='590/80d',  marker='o', markersize=1)
ax[1].plot(np.arange(0.5,511.5,1), c1ds, label='600/40ds', linewidth=2)
ax[1].plot(np.arange(0.5,511.5,1), c2ds, label='700LPds', linewidth=2)
ax[1].plot(np.arange(0.5,511.5,1), c3ds, label='590/80ds', linewidth=2)
ax[2].plot(np.arange(0,512,1), p)
ax[2].scatter(slope_max, [580,620,700,550,630])
ax[0].set_ylabel('%T')
ax[1].set_ylabel('d(T)')
ax[2].set_ylabel('Wavelength (nm)')
ax[2].set_xlabel('Pixel')
ax[0].set_xlim(0,col)
ax[0].legend(loc=2, frameon='None')
ax[1].legend(loc=2, frameon='None')



fig, ax = plt.subplots()
ax.imshow(movie[:,:], cmap='gray')
plt.title('Image')
pt = np.array(plt.ginput(n=0, timeout=0, show_clicks=True))
ax.plot(pt[:,0], pt[:,1], 'r+')
ax.set_xlim(0,col)
ax.set_ylim(row,0)
fig.canvas.draw()


fig, ax = plt.subplots(len(pt)*4)
for i in range(len(pt)):
    spec = np.mean(movie[pt[i,1]-scan:pt[i,1]+scan, :], axis=0)
    bg = np.mean(movie[pt[i,1]-scan-displacement:pt[i,1]+scan-displacement, :], axis=0)
    spec_bgcr = spec-bg
    
    ax[i*4].imshow(movie[pt[i,1]-scan:pt[i,1]+scan, :], cmap='gray')
    ax[i*4+1].imshow(movie[pt[i,1]-scan-displacement:pt[i,1]+scan-displacement, :], cmap='gray')    
    ax[i*4+2].plot(p, spec)
    ax[i*4+2].plot(p, bg)
    ax[i*4+3].plot(p, spec_bgcr)
    ax[i*4+2].set_xlim(p.min(), p.max())
    ax[i*4+3].set_xlim(p.min(), p.max())
    
    print np.sum(spec_bgcr)