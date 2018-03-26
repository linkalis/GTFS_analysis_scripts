import arcpy

inFC = 'mpls_stpaul_stops_projected'
outFC = 'mpls_stpaul_stops_projected_buffered'


arcpy.Buffer_analysis(inFC, outFC, "0.5 miles", dissolveType = "ALL")
