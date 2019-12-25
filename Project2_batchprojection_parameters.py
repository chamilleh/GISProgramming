#File: Project2_batchprojection_parameters
#Pennsylvania State University
#Geog 485: Project 2 Assignment
#Author: Chamille Hartman October2019

#This script functions as a tool in geoprocessing environment, so that it performs a batch reprojection of vector datasets.
#The data used in this script is provided as part of Lesson 2.
#Data was obtained from Washington State Department of Transportation GeoData Distribution Catalog.
#Resources used:https://community.esri.com/thread/22466, https://pro.arcgis.com/en/pro-app/tool-reference/data-management/project.htm, https://pro.arcgis.com/en/pro-app/arcpy/functions/listfeatureclasses.htm

import arcpy

try:

    # set environments and path for where to save the reprojected shapefile
    targetFolder = arcpy.GetParameterAsText(0)
    arcpy.env.workspace = targetFolder
    arcpy.env.overwriteOutput = True

    # extract spatial reference information from the desired projection
    targetProjectionPath = arcpy.GetParameterAsText(1)
    targetDesc = arcpy.Describe(targetProjectionPath)
    targetSR = targetDesc.spatialReference
    targetProjection = targetSR.name

    #creates a list of shapefiles to reproject
    shapeFileList = arcpy.ListFeatureClasses()

    #Walk through the list of shapefiles to check on spatial reference match.
    #if not it will move to the else clause to perform a reprojection and change the file name
    for shapeFile in shapeFileList:
        desc = arcpy.Describe(shapeFile)
        spatialRef = desc.spatialReference
        spatialName = spatialRef.name
        if spatialName == targetProjection:
            arcpy.AddMessage(shapeFile + " is already in " + targetProjection)
        else:
            newFile = shapeFile.replace(".shp", "_projected.shp")
            newProjection = arcpy.Project_management(shapeFile, newFile, targetSR)
            #prints a list of reprojected shapefiles
            for projection in newProjection:
                arcpy.AddMessage(newFile)

except:
    #Report if there was an error
    arcpy.AddMessage(arcpy.GetMessages())