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

cursor = arcpy.da.SearchCursor(outFC_envolope, ['Shape_Area'])
for row in cursor:
    total_coverage_area = row[0]
    print('TOTAL COVERAGE AREA: ' + str(total_coverage_area))


cursor = arcpy.da.SearchCursor(outFC_buffer, ['Shape_Area'])
for row in cursor:
    print('NEAR TRANSIT AREA: ' + str(row[0]))

total_stops = arcpy.GetCount_management(inFC)
stop_density = total_stops / total_coverage_area

print('STOP DENSITY: ' + str(stop_density))
