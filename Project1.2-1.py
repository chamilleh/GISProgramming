#Name: Project1.2.py
#Geog 485 Project 1 Part 2
#author: Chamille Hartman October 2019

#The purpose of this script is to create contour lines from a raster dataset of Fox Lake, Utah.
#The tool used in this script is Contour in the Spatial Analyst toolbox.
#Resources used: http://desktop.arcgis.com/en/arcmap/10.3/tools/defense-mapping-toolbox/create-contours.htm
#http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00150000000p000000.htm
#Required: import spatial analyst extension (sa) as well as the arcpy module



import arcpy.sa
arcpy.env.overwriteOutput = True

try:
    #path of where the raster data is located
    #path of where the processed data is to be saved
    rasterData = "D:/GIS Certificate/GEOINT/GEOG485- Web Dev Map/Lesson1/data/foxlake"
    outputFolder = "D:/GIS Certificate/GEOINT/GEOG485- Web Dev Map/Lesson1/Project1/scriptresults/outcontourtest.shp"

    #prints a message indicating the script running
    arcpy.AddMessage("Contouring...")

    # check out spatial analyst extension
    arcpy.CheckOutExtension("Spatial")

    #contour variables provides the distance and frequency of the contour lines.
    contourInt = 25
    contourBase = 0

    #Perform Contour tool
    arcpy.sa.Contour(rasterData, outputFolder, contourInt, contourBase)

    #Prints a message if tool performs successfully
    arcpy.AddMessage("Completed processing")

except:
    #Print the following error message when tool fails
    arcpy.AddError("Failed Execution")

    #Prints any error messages
    arcpy.AddMessage(arcpy.GetMessage(0))

#Check in Spatial Analyst extension
arcpy.CheckInExtension("Spatial")


