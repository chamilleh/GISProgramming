# File: HartmanC_finalproj
# Pennsylvania State University
# Geog 485: Final Project
# Fall 2 2019
# Author: Chamille Hartman December2019

# resources used: various Esri documentation

# This is a script that would allow the user to further leverage the power of data driven pages.
# This code takes the functionality of data driven pages and allows for some customization and automation.
# Specifically written for converting shapefiles into layer files


import arcpy
arcpy.env.overwriteOutput = True

def createTextTitleElement(lyrfile, mapdoc):
    # Identify required fields
    fields = ["PWS_ID", "PWS_Label", "SRC_Label"]
    # Perform search cursor only on the set of selected attributes
    with arcpy.da.SearchCursor(lyrfile, fields) as cursor:
        for r in cursor:
            # Assign variable which will be used in the heading element
            for elm in arcpy.mapping.ListLayoutElements(mapdoc, "TEXT_ELEMENT", "*Title*"):
                elm.text = ('Figure 2: {} PWS {} \r\n{} Groundwater Source Area'.format(r[1], r[0], r[2]))

# The following variables are sample for testing
sampleOutput = r"C:\Users\Chamille\Desktop\SampleMap.pdf"
samplePWS = "PWS_ID = '4100682'"
sampleSRC = "SRC_Label LIKE '%Lamonta%'"


layerFile = r"G:\GIS Certificate\GEOINT\GEOG485_WebDevMap\FinalProject\data\dwp-orgwdwsa\OR_groundwater.shp"

# File to map layout in the form of an mxd.
# File needs to be saved to local drive in order to access or
# Create a copy mxd file to a local spot then delete
mxd = arcpy.mapping.MapDocument(r"C:\Users\Chamille\Desktop\groundwatermaps.mxd")

# Makes a temporary feature layer from a shapefile
shpLayer = arcpy.MakeFeatureLayer_management(layerFile, "Groundwater Polygons")
shpLayerCopy = arcpy.SaveToLayerFile_management(shpLayer, "Groundwaterpoly.lyr", "RELATIVE")
# TO BE DELETED AFTER pdf CREATION

# Add layers to datasets
# Reference layer file
inputData = arcpy.mapping.Layer(r"C:\Users\Chamille\Desktop\Groundwaterpoly.lyr")
# Loop to add layer file to both inset and main map

for df in arcpy.mapping.ListDataFrames(mxd):
    if df.name == "Inset Map":
        arcpy.mapping.AddLayer(df, inputData)
        dfInset = df
    elif df.name == "Main Map":
        arcpy.mapping.AddLayer(df, inputData)
        dfMain = df
    else:
       print("No data frame available")


# MAIN MAP
# Start for loop to isolate specific indexing layer
for lyr in arcpy.mapping.ListLayers(mxd):
    # Select specific identifying attribute
    arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", sampleSRC)
    # call function to change title based on selected feature
    createTextTitleElement(lyr, mxd)
    # Zoom to current selection's extent
    dfMain.extent = lyr.getSelectedExtent()


# INSET MAP
# Set the extent of the inset map zoomed out to 200%
dfInset.extent = dfMain.extent
dfInset.scale = dfInset.scale*2


# Exports map as pdf. To export an entire layout, PAGE_LAYOUT parameter.
# For a specific data frame, reference listed data frames.
arcpy.mapping.ExportToPDF(mxd, sampleOutput, 'PAGE_LAYOUT')




