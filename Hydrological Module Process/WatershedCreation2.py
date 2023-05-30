# -------------------------------------------------------------------------
# Name:        Watershed Creation 
# Purpose:     Extract Watershed from Dem
#
# Author:      Elham soleimanian
#
# Created:     17/10/2020
# -------------------------------------------------------------------------
# Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import geopandas as gpd
# import mplleaflet
from pysheds.grid import Grid
#-------------------------------------------------------------------------
# Open Digital Elevation Model 
grid  = Grid.from_raster(r'D:\WatershedStreamNetworkDelimitationwithPythonandPysheds\Rst\LocalDem.tif', data_name = 'dem')
#-------------------------------------------------------------------------
# Define a Function to plot 
def plotFigure(data, label, cmap = 'Blues'):
    """ 
    This Function loads and plot Data
    """
    plt.figure(figsize = (12,10))
    plt.imshow(data, extent = grid.extent, cmap= cmap)
    plt.colorbar(label = label)
    plt.grid()
    
# Minor Sclicing to enhance colorbar 
elevDem =grid.dem[:-1,:-1]
# Show Dem
plotFigure(grid.dem , 'Elevation(m)')

# Detect Depressions 
depressions = grid.detect_depressions('dem')
plotFigure(depressions,'dep')

grid.fill_depressions(data='dem',out_names='flooded_dem')
depressions= grid.detect_depressions('flooded_dem')
plotFigure(depressions,'dep')
#------------------------------------------------------------------------
# detect flat
flats = grid.detect_flats('flooded_dem')
plotFigure(flats,'dep')
grid.resolve_flats(data='flooded_dem',out_name='inflated_dem')
plt.imshow(grid.inflated_dem[:-1,:-1])
# Define direction Map 
# N NE E SE S SN W NW
dirmap = (64 , 128, 1, 2, 4, 8, 16, 32)

# Create Flow Direction  
grid.flowdir(data='inflated_dem', out_name='dir', dirmap=dirmap)
plotFigure(grid.dir,'Flow Directiom','viridis')
# Define Catchment
# Specify pour point
x, y = 45.916351,37.337377
# Delineate the catchment
grid.catchment(data='dir', x=x, y=y, dirmap=dirmap, out_name='catch',
               recursionlimit=60000, xytype='label', nodata_out=0)


# Clip the bounding box to the catchment
grid.clip_to('catch')

# Get a view of the catchment
demView = grid.view('dem', nodata=np.nan)
plotFigure(demView,'Elevation')

#export selected raster
grid.to_raster(demView, r'D:/WatershedStreamNetworkDelimitationwithPythonandPysheds/Output/clippedElevations_WGS84.tif')
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
# ax = streamNet.plot()
# mplleaflet.display(fig=ax.figure, crs=streamNet.crs, tiles='esri_aerial')