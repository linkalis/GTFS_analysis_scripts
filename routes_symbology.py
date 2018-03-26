from arcpy import *

aprx = arcpy.mp.ArcGISProject('CURRENT')

aprx.defaultGeodatabase = "X:\\GIS5572\\GIS5572_PosterProject\\GTFSAnalysis\\GTFSAnalysis.gdb"

m = aprx.listMaps('Map')[0]

lyr = m.listLayers()[0]

#for lyr in m.listLayers():
    if lyr.isBasemapLayer:
        continue # proceed to next layer, but don't do anything to basemap layers

#print(lyr.dataSource)
sym = lyr.symbology
sym.updateRenderer('UniqueValueRenderer')
sym.renderer.fields = ['route_type']
sym.renderer.addValues({"Tram-Streetcar-Lightrail" : ["0"]})
