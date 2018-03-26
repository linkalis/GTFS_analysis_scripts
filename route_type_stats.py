# Dissolve routes and compute route type statistics

import arcpy
import numpy as np
import SSDataObject as ssdo

inFC = 'mpls_stpaul_shapes_projected'
outFC = 'mpls_stpaul_shapes_projected_dissolved'

# Need to dissolve on route_type alone to avoid double-counting parts of the
# networks where multiple routes use the same road/rail infrastructure
Dissolve_management(
    inFC,
    outFC,
    dissolve_field = ["route_type"],
    statistics_fields = [["OBJECTID", "COUNT"], ["route_id", "COUNT"]],
    multi_part = "MULTI_PART",
    unsplit_lines = "DISSOLVE_LINES"
)

# Convert output feature class to a spatial statistics data object
# so we can perform pandas data manipulation on it
dataobject = ssdo.SSDataObject(outFC)

#dataobject.allFields # show available fields
dataobject.obtainData(dataobject.oidName, ['ROUTE_TYPE', 'SHAPE_LENGTH'])
df = dataobject.getDataFrame()

# Get total length of transit infrastructure
total_length = df['SHAPE_LENGTH'].sum()
print("TOTAL LENGTH: " + str(total_length))

# Compute percent of total that each route type represents
df['PERCENT'] = df['SHAPE_LENGTH'] / total_length * 100

print(df)
