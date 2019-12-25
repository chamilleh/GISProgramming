# File: project3_extractingdata
# Pennsylvania State University
# Geog 485: Project 3 Assignment
# Author: Chamille Hartman November2019

# resources used: https://www.programiz.com/python-programming/string-interpolation
# https://www.w3schools.com/python/ref_func_map.asp

# This script allows the user to create separate shapefiles based on user input query.

import arcpy
# define paths and set up environment
arcpy.env.workspace = r"C:\KJK\PSU\485_Material\Lesson3\Data"
arcpy.env.overwriteOutput = True


# create functions to convert height and weight into metric system to be called in the UpdateCursor loop
def metric_convert(height):
    split_string = height.replace("\"", "").split("'")  # removes special characters from field data
    integer_array = map(int, split_string)  # converts the two string numbers into integers
    array_height = list(integer_array)  # creates a list of the new integers
    inch_height = array_height[0] * 12 + array_height[1]  # calculates the integers into inches
    cm_height = inch_height * 2.54  # converts the integers into centimeters
    return cm_height


def kilo_convert(weight):
    kg_weight = weight * 0.453592  # converts weight into kilograms
    return kg_weight


# define target feature layer, and query for selection
targetCountryLayer = "Countries_WGS84.shp"
queryCountry = "CNTRY_NAME = 'Sweden'"
targetNHLLayer = r"C:\KJK\PSU\485_Material\Lesson3\Data\nhlrosters.shp"


# create a layer of sweden
layerCountry = arcpy.MakeFeatureLayer_management(targetCountryLayer, "country_lyr", queryCountry)
##layerSweden = arcpy.SelectLayerByAttribute_management(layerCountry, 'NEW_SELECTION', queryCountry)

### create nhl roster layer to be used as parameter for selection
##layerNHL = arcpy.MakeFeatureLayer_management(targetNHLLayer, "nhl_temp")

# define a tuple list of attributes to use in selection
targetPosition = ['RW', 'LW', 'C']

try:
    # loops through the desired positions and performs a selection, then creates a new file
    for position in targetPosition:
        queryPosition = "position = '%s'" % (position)
        # KJK- make a feature layer of the position instead of selecting
        layerNHL = arcpy.MakeFeatureLayer_management(targetNHLLayer, "nhl_temp", queryPosition)
##        selectPosition = arcpy.SelectLayerByAttribute_management(selectINCountry, 'NEW_SELECTION', queryPosition)
        selectINCountry = arcpy.SelectLayerByLocation_management(layerNHL, "WITHIN", layerCountry)
        newShapefile = arcpy.CopyFeatures_management(selectINCountry, position)
        # adds two new fields to the new shapefiles
##        arcpy.AddFields_management(newShapefile, [['height_cm', 'Float'], ['weight_kg', 'Float']])
        arcpy.AddField_management(newShapefile, "height_cm", "FLOAT")
        arcpy.AddField_management(newShapefile, "weight_kg", "FLOAT")

        # populates the two new rows with converted height and weight
        with arcpy.da.UpdateCursor(newShapefile, ['height', 'weight', 'height_cm', 'weight_kg']) as cursor:
            for row in cursor:
                height_cm = metric_convert(row[0])
                weight_kg = kilo_convert(row[1])
                row[2] = height_cm
                row[3] = weight_kg
                cursor.updateRow(row)
            del cursor
            del row

except:
    print(arcpy.GetMessages())


