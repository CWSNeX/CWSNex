# -------------------------------------------------------------------------
# Name:        Watershed Creation 
# Purpose:     Extract Watershed from Dem
#
# Author:      Elham soleimanian
#
# Created:     17/10/2020
# -------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.colors as colors
import geopandas as gpd
from pysheds.grid import Grid
import mplleaflet
#-------------------------------------------
#open Dem File
grid  = Grid.from_raster(r'D:\WatershedStreamNetworkDelimitationwithPythonandPysheds\Rst\LocalDem.tif', data_name = 'dem')
def plotFigure(data, label, cmap = 'Blues'):
    """ 
    This Function loads and plot Data
    """
    plt.figure(figsize = (12,10))
    plt.imshow(data, extent = grid.extent, cmap= cmap)
    plt.colorbar(label = label)
    plt.grid()
# Show Dem
plotFigure(grid.dem , 'Elevation(m)')
#------------------------------------------
# Define direction Map 
# N NE E SE S SN W NW
dirmap = (64 , 128, 1, 2, 4, 8, 16, 32)
# Create Flow Direction  
grid.flowdir(data='dem', out_name='dir', dirmap=dirmap)
plotFigure(grid.dir,'Flow Directiom','viridis')
#------------------------------------------
# Define Catchment
# Specify pour point
x, y = 45.90069444448125,37.35680555558539
#------------------------------------------
# Delineate the catchment
grid.catchment(data='dir', x=x, y=y, dirmap=dirmap, out_name='catch',
               recursionlimit=15000, xytype='label', nodata_out=0)
#------------------------------------------
# Clip the bounding box to the catchment
grid.clip_to('catch')
#------------------------------------------
# Get a view of the catchment
demView = grid.view('dem', nodata=np.nan)
plotFigure(demView,'Elevation')
#------------------------------------------
#export selected raster
grid.to_raster(demView, r'D:/WatershedStreamNetworkDelimitationwithPythonandPysheds/Output/clippedElevations.tif')

#------------------------------------------
#Define accumulation grid and stream network
grid.accumulation(data='catch', dirmap=dirmap, pad_inplace=False, out_name='acc')
accView = grid.view('acc', nodata=np.nan)
plotFigure(accView,"Cell Number",'PuRd')
streams = grid.extract_river_network('catch', 'acc', threshold=200, dirmap=dirmap)
streams["features"][:2]
def saveDict(dic,file):
    f = open(file,'w')
    f.write(str(dic))
    f.close()
#save geojson as separate file
saveDict(streams,r'D:/WatershedStreamNetworkDelimitationwithPythonandPysheds/Output/streams.geojson')


#Plot DEM and stream network on Web
streamNet = gpd.read_file(r'D:/WatershedStreamNetworkDelimitationwithPythonandPysheds/Output/streams.geojson')
streamNet.crs = {'init' :'epsg:2436'}

#-------------------------------------------
# The polygonize argument defaults to the grid mask when no arguments are supplied
shapes = grid.polygonize()

# Plot catchment boundaries
fig, ax = plt.subplots(figsize=(6.5, 6.5))

for shape in shapes:
    coords = np.asarray(shape[0]['coordinates'][0])
    ax.plot(coords[:,0], coords[:,1], color='cyan')

ax.set_xlim(grid.bbox[0], grid.bbox[2])
ax.set_ylim(grid.bbox[1], grid.bbox[3])
ax.set_title('Catchment boundary (vector)')
gpd.plotting.plot_dataframe(streamNet, None, cmap='Blues', ax=ax)
#ax = streamNet.plot()
# mplleaflet.display(fig=ax.figure, crs=streamNet.crs, tiles='esri_aerial')



