import arcpy
import numpy as np
import SSDataObject as ssdo


# Dissolve on route_id:
Dissolve_management("berlin_VBB_GTFS_route_shapes", "berlin_VBB_GTFS_route_shapes_dissolved", ["route_id", "route_short_name", “route_type”], [["OBJECTID", "COUNT"]], "MULTI_PART", "DISSOLVE_LINES")


# Coverage area analysis:
# “Minimum Bounding Geometry”: http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/minimum-bounding-geometry.htm)

# <Buffer within 1/2mile of all stops (AllTransit's methodology), then get bounding box>
arcpy.MinimumBoundingGeometry_management('berlin_VBB_GTFS_route_shapes',’berlin_bb’, "CONVEX_HULL", "ALL")


# Number of transit routes & longest route analysis

# Convert to a spatial statistics data object
fc = r'berlin_VBB_GTFS_route_shapes_dissolved_projected'
dataobject = ssdo.SSDataObject(fc)

dir(dataobject) # get all methods available for this type of object

# Convert to a data frame
dataobject.allFields
dataobject.obtainData(dataobject.oidName, ['ROUTE_ID', 'ROUTE_SHORT_NAME', 'SHAPE_LENGTH'])
df = dataobject.getDataFrame()
print(df.head())

# Then use pandas data frame methods to get the longest and shortest routes
df_sorted = df.sort_values(by=['SHAPE_LENGTH'], ascending=False).round(decimals = 6)
longest_5_length = df_sorted.iloc[5,2]
select_clause = """"Shape_Length" >= """ + str(longest_5_length)
arcpy.SelectLayerByAttribute_management('berlin_VBB_GTFS_route_shapes_dissolved_projected', "NEW_SELECTION", select_clause)

shortest_5_length = df_sorted.iloc[-5,2]
select_clause = """"Shape_Length" <= """ + str(shortest_5_length)
arcpy.SelectLayerByAttribute_management('berlin_VBB_GTFS_route_shapes_dissolved_projected', "NEW_SELECTION", select_clause)


And highlight it using select and symbology:



Highlight/select high-frequency lines into a separate shapefile


Cluster bus stops to detect “transit neighborhoods”

https://community.esri.com/groups/spatial-data-science/blog/2016/02/11/connecting-arcpy-to-your-jupyter-notebook
