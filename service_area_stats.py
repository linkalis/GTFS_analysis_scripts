#############################
## SERVICE AREA STATISTICS ##
#############################

# Purpose: Compute service area statistics to calculate amount of coverage area
# and extent of "near-transit" areas from GTFS stops data and print results
# to the console

# Load required libraries
import arcpy

# Set a default workspace to save buffer and convex hull envelope polygon
# feature classes that are derived when running this script, and that power
# the statistics being calculated
main_ws = "C:\\path\\to\\your\\project\\folder\\GTFSAnalysis.gdb" # point this to the default geodatabase within your active project
arcpy.env.workspace = main_ws

# Set inputs and outputs
inFC = 'rome_stops_projected'
outFC_buffer = 'rome_stops_projected_buffered_geodesic'
outFC_envelope = 'rome_service_area_envelope'

# Buffer the stops data using a geodesic buffer for more accurate measurments
# (especially for areas near the edges of UTM zones).  Set buffer distanct to 0.5
# miles to align with other "near-transit" analysis methodologies.  Or, adjust
# this value as necessary.
arcpy.Buffer_analysis(inFC, outFC_buffer, "0.5 miles", dissolve_option = "ALL", method = "GEODESIC")

# Calculate a convex hull minimum bounding polygon to get the perimeter of
# the coverage area for this GTFS data
arcpy.MinimumBoundingGeometry_management(outFC_buffer,
                                         outFC_envelope,
                                         "CONVEX_HULL", "NONE")

# Now, compute three statistics using the polygons generated above.  Print each
# statistic to the console once it's computed:

# 1) The total coverage area -- the area of the convex hull bounding envelope)
cursor = arcpy.da.SearchCursor(outFC_envelope, ['Shape_Area'])
for row in cursor:
    total_coverage_area = row[0] * 0.000001 # multiplier to convert from meters (UTM default) to km
    print('TOTAL COVERAGE AREA: ' + str(total_coverage_area) + " sq km")

# 2) The 'near-transit area' -- the area that falls within the stops buffer
cursor = arcpy.da.SearchCursor(outFC_buffer, ['Shape_Area'])
for row in cursor:
    near_transit_area = row[0] * 0.000001 # multiplier to convert from meters (the UTM default) to km
    print('NEAR TRANSIT AREA: ' + str(near_transit_area)  + " sq km")

# 3) The stop density -- the number of stops divided by the total coverage area
total_stops = arcpy.GetCount_management(inFC)[0]
stop_density = float(total_stops) / total_coverage_area
print('STOP DENSITY: ' + str(stop_density)  + " per sq km")
