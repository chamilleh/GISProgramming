# file: HartmanC_project4_rhinofiles.py
# Pennsylvania State University
# Geog 485 Fall2 2019
# author: Chamille Hartman

# This script takes a csv file, creates a dictionary of target data, and loops
# the data to create a polyline.




import arcpy
import csv

# Arcpy environment settings
arcpy.env.overwriteOutput = True   ## Not always necessary. In this instance, it is in place for testing purposes
arcpy.env.workspace = r"F:\GIS Certificate\GEOINT\GEOG485_WebDevMap\Lesson4"
output = r"F:\GIS Certificate\GEOINT\GEOG485_WebDevMap\Lesson4\output"

# Create a geodatabase for featurelayer

# Create a spatial reference for use in creating a new feature class
spatialRef = arcpy.SpatialReference("Geographic Coordinate Systems/World/WGS 1984")

# Create an empty feature class to create the polyline onto. Change out_name to appropriate syntax for geodatabase type of output.
rhinoFile = arcpy.CreateFeatureclass_management(out_path=output, out_name="RhinoTracking.shp", geometry_type="POLYLINE", spatial_reference=spatialRef)


# Ask to open the csv file in read only mode
rhinoTrack = open("F:\GIS Certificate\GEOINT\GEOG485_WebDevMap\Lesson4\RhinoObservations.csv", "r")

# Set up csv reader and identifies the headers
csvReader = csv.reader(rhinoTrack)
csvHeader = next(csvReader)

# Index of target headers
latData = csvHeader.index("X")
lonData = csvHeader.index("Y")
rhinoName = csvHeader.index("Rhino")

# An empty dictionary to write target fields onto
rhinoDictionary = {}

# Loop to read each line. Associate variables to the appropriate header
for row in csvReader:
    rhinoNames = row[rhinoName]
    latitudeVal = row[latData]
    longitudeVal = row[lonData]

    # Check if key, rhinoNames, is already in the dictionary. If not create a new key.
    # Assign long lat values as paired arrays to the appropriate key
    if rhinoNames not in rhinoDictionary:
        rhinoDictionary[rhinoNames] = [arcpy.Point(latitudeVal, longitudeVal)]
    else:
        rhinoDictionary[rhinoNames].append(arcpy.Point(latitudeVal, longitudeVal))


# create point geometries
nameKey = list(rhinoDictionary.keys())
polyArray = []
for val in nameKey:
    rhinoArray = arcpy.Array(rhinoDictionary[val])     # grabs the values based on the val from boval
    trackPoly = arcpy.Polyline(rhinoArray, spatialRef)
    polyArray.append(trackPoly)

# Copy the list if polylines to the feature layer
arcpy.CopyFeatures_management(polyArray, rhinoFile)


# Add a new field for the Rhino name
arcpy.AddField_management(rhinoFile, 'name', 'TEXT')

index = 0
with arcpy.da.UpdateCursor(rhinoFile, ["name"]) as cursor:
    for row in cursor:
        row[0] = nameKey[index]
        cursor.updateRow(row)
        index = index + 1
    del cursor
    del row





# Copy features onto the empty polyline feature













