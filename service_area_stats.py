

# Load required libraries
import arcpy


main_ws = "X:\\GIS5572\\GIS5572_PosterProject\\GTFSAnalysis\\GTFSAnalysis.gdb"
arcpy.env.workspace = main_ws

inFC = 'rome_stops_projected'
outFC_buffer = 'rome_stops_projected_buffered_geodesic'
outFC_envelope = 'rome_service_area_envelope'

# Use geodesic buffer for more accurate measurments
# (especially for areas near the edges of UTM zones)
arcpy.Buffer_analysis(inFC, outFC_buffer, "0.5 miles", dissolve_option = "ALL", method = "GEODESIC")

arcpy.MinimumBoundingGeometry_management(outFC_buffer,
                                         outFC_envelope,
                                         "CONVEX_HULL", "NONE")

cursor = arcpy.da.SearchCursor(outFC_envelope, ['Shape_Area'])
for row in cursor:
    total_coverage_area = row[0] * 0.000001
    print('TOTAL COVERAGE AREA: ' + str(total_coverage_area) + " sq km")


cursor = arcpy.da.SearchCursor(outFC_buffer, ['Shape_Area'])
for row in cursor:
    near_transit_area = row[0] * 0.000001
    print('NEAR TRANSIT AREA: ' + str(near_transit_area)  + " sq km")

total_stops = arcpy.GetCount_management(inFC)[0]
stop_density = float(total_stops) / total_coverage_area

print('STOP DENSITY: ' + str(stop_density)  + " per sq km")
