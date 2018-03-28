# Auto-Project to correct UTM zone

from arcpy import *

# Define inputs and outputs
inFC = 'mpls_stpaul_shapes'
outFC = 'mpls_stpaul_shapes_projected'

# Manage environments
# http://pro.arcgis.com/en/pro-app/tool-reference/environment-settings/scratch-workspace.htm
main_ws = "X:\\GIS5572\\GIS5572_PosterProject\\GTFSAnalysis\\GTFSAnalysis.gdb"
scratch_ws = "X:\\GIS5572\\GIS5572_PosterProject\\GTFSAnalysis"

# Switch to scratch workspace
arcpy.env.scratchWorkspace = scratch_ws # initialize the scratch workspace
arcpy.env.workspace = arcpy.env.scratchGDB # point to the scratch geodatabase as target for storing intermediate data
#arcpy.env.workspace = arcpy.env.scratchFolder # point to the scratch folder (shapefiles) as target for storing intermediate data

# Load UTM zone data into map
# Note: A feature class called 'utm' must be available in the project's main geodatabase
aprx = arcpy.mp.ArcGISProject("CURRENT")
map = aprx.listMaps()[0]  # add data to first map listed
utm_layer = map.addDataFromPath(main_ws + "\\utm")

# Get a bounding box envelope
arcpy.MinimumBoundingGeometry_management(inFC , 'bounding_box', "ENVELOPE", "ALL")

# Get centroid
# https://support.esri.com/en/technical-article/000011754
cursor = arcpy.da.SearchCursor('bounding_box', "SHAPE@XY")

centroid_coords = []
for feature in cursor:
    centroid_coords.append(feature[0])

# Convert to Point
centroidpoint = arcpy.Point()
pointGeometryList = []

for pt in centroid_coords:
    centroidpoint.X = pt[0]
    centroidpoint.Y = pt[1]

    pointGeometry = arcpy.PointGeometry(centroidpoint)
    pointGeometryList.append(pointGeometry)

arcpy.CopyFeatures_management(pointGeometryList, 'centroid_point') # copy centroid point to gdb


# Detect UTM zone based on centroid point
#arcpy.ListSpatialReferences("*WGS 1984 UTM Zone*")

# Spatial join on centroid and UTM feature class to get UTM intersect
arcpy.SpatialJoin_analysis('centroid_point', 'utm', 'centroid_utm')

cursor = arcpy.da.SearchCursor('centroid_utm', ['ZONE', 'SHAPE@Y'])
for row in cursor:
    utm_zone = row[0]
    y_coord = row[1]

# Decide whether to use N or S UTM zones based on Y-coord value
if y_coord > 0:
    srs = 'WGS 1984 UTM Zone ' + str(utm_zone) + 'N'
elif y_coord <= 0:
    srs = 'WGS 1984 UTM Zone ' + str(utm_zone) + 'S'
else:
    print('Sorry! Couldn’t detect SRS.')

# Project data
arcpy.env.workspace = main_ws # switch back to main workspace
out_coordinate_system = arcpy.SpatialReference(srs)
arcpy.Project_management(inFC, outFC, out_coordinate_system)

# Clean up scratch workspace
arcpy.Delete_management(arcpy.env.scratchGDB)
map.removeLayer(utm_layer)
