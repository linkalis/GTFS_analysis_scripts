############################################
## ROUTE TYPE STATISTICS - ArcGIS Toolbox ##
############################################

# Purpose: Compute the percentage of each route type that is present in a
# GTFS dataset and save the results to a table in the default project geodatabase

# Load required libraries
import arcpy
import numpy as np
import SSDataObject as ssdo

# Read parameters from the toolbox front end
inFC = arcpy.GetParameterAsText(0)
outTable = arcpy.GetParameterAsText(1)
dissolvedFC = 'dissolvedFC'

arcpy.AddMessage("Table will be saved to: " + outTable)

arcpy.SetProgressorLabel("Dissolving routes by route type...") # Update the user on our progress so far

# Dissolve the input shapes/routes feature class using 'route_type' as a dissolve field.
# This avoids double-counting parts of the networks where multiple routes use
# the same road/rail infrastructure.
arcpy.Dissolve_management(
    inFC,
    dissolvedFC,
    dissolve_field = ["route_type"],
    statistics_fields = [["OBJECTID", "COUNT"], ["route_id", "COUNT"]],
    multi_part = "MULTI_PART",
    unsplit_lines = "DISSOLVE_LINES"
)

arcpy.SetProgressorLabel("Computing route statistics...")

# Convert output feature class to a spatial statistics data object
# so we can perform pandas data manipulation on it
dataobject = ssdo.SSDataObject(dissolvedFC)

#dataobject.allFields # show available fields
dataobject.obtainData(dataobject.oidName, ['ROUTE_TYPE', 'SHAPE_LENGTH'])
df = dataobject.getDataFrame()

# Get total length of transit infrastructure so we can use it for calculating
# route type percentages, and also display it along with the completion message
# when the tool is done running
total_length = df['SHAPE_LENGTH'].sum()
print("TOTAL LENGTH: " + str(total_length))

# Compute percent of total that each route type represents
df['PERCENT'] = df['SHAPE_LENGTH'] / total_length * 100

# Define a dictionary containing the route types that are part of the GTFS standards.
# Set this up as a regex-based dictionary, so we can add a final catch-all pattern
# at the end of the dictionary to catch the 'extended' route types or other unrecognized
# numeric values that are not part of the standard set of route types.
# The '^...$' pattern forces an exact string match; the '[0-9]{2,}' pattern looks
# for any number that is two or more digits long
route_types_dict = {
    "^0$" : "Tram, Streetcar, Light rail",
    "^1$" : "Subway, Metro",
    "^2$" : "Rail",
    "^3$" : "Bus",
    "^4$" : "Ferry",
    "^5$" : "Cable car",
    "^6$" : "Gondola, Suspended cable car",
    "^7$" : "Funicular",
    "(^8$|^9$|[0-9]{2,})": "Unknown"
}

# Create a copy of the 'ROUTE_TYPE' column, but coerce it into a string for matching.
# Then remap its values to the descriptions provided in the dictionary above using
# regex mapping.
df['ROUTE_TYPE_DESCRIPTION'] = df['ROUTE_TYPE'].map(str)
df['ROUTE_TYPE_DESCRIPTION'].replace(route_types_dict, regex=True, inplace=True)

arcpy.AddMessage(df)

# Convert the spatial statistics data object (which is formatted as a pandas data frame)
# to a numpy array using the to_records() method.
df_as_nparray = df.to_records(index=False)
arcpy.AddMessage(df_as_nparray.dtype)
np_df = np.array(df_as_nparray, dtype = [("ROUTE_TYPE", int),
                                     ("ROUTE_TYPE_DESCR", "|S256"),
                                     ("PERCENT", float),
                                     ("SHAPE_LENGTH", float)])

arcpy.AddMessage(np_df.dtype)
arcpy.AddMessage(np_df)

# Use ArcPy's data access (da) module's NumPyArrayToTable() function to convert
# the newly-formatted numpy array to a table that can be stored in the default workspace
arcpy.da.NumPyArrayToTable(np_df, outTable)

# Send a completion message to the tool dialog box
arcpy.SetProgressorLabel("Success! Statistics table generated and save to default workspace.")
arcpy.AddMessage("Total route length: " + str(total_length))
