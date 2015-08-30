# This module should be called from a ArcGIS toolbox classic (not .pyt)
# This module will call SDEedit_execute.py for the actual work :-)


#------

# http://resources.arcgis.com/en/help/main/10.2/index.html#//018w00000005000000
# http://gis.stackexchange.com/questions/119938/error-with-da-updatecursor-and-sde-feature-classes

import arcpy
import os

#===============================================================================
# fc = 'Database Connections\nis_editor@green3.sde\NIS.Vores_Navne\NIS.NamesAtest'
# str_ws = os.path.dirname(fc)
# print "ws: "+str(str_ws)
# 
# # Start an edit session. Must provide the worksapce.
# edit = arcpy.da.Editor(str_ws)
# 
# # Edit session is started without an undo/redo stack for versioned data
# #  (for second argument, use False for unversioned data)
# edit.startEditing(False, True)
# 
# # Start an edit operation
# edit.startOperation()
# 
# # Insert a row into the table.
# with arcpy.da.InsertCursor(fc, ('SHAPE@', 'Name')) as icur:
#     icur.insertRow([(7642471.100, 686465.725), 'New School'])
# 
# # Stop the edit operation.
# edit.stopOperation()
# 
# # Stop the edit session and save the changes
# edit.stopEditing(True)
# 
#  
# import os
# import arcpy
#  
#===============================================================================

#===============================================================================
# arcpy.env.workspace = r"C:\Users\mahvi\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\nis_editor@green3.sde"
# lst_fdss = arcpy.ListDatasets("*", "Feature") 
# print "fds: "+str(lst_fdss)
# for fds in lst_fdss: 
#     if "Vores_Navne" in fds:
#         print "feature data set: "+fds
#         print " -         baseName: " + arcpy.Describe(fds).baseName
#         print " -      catalogPath: " + arcpy.Describe(fds).catalogPath
#         print " -  dataElementType: " + arcpy.Describe(fds).dataElementType
#         print " -         dataType: " + arcpy.Describe(fds).dataType
#         print " -             name: " + arcpy.Describe(fds).name
#         print " -             path: " + arcpy.Describe(fds).path
#         
#           
#         fcList = arcpy.ListFeatureClasses("*","",fds)  
#         for fc in fcList:  
#             print "    feature class: "+fc 
#===============================================================================
 
 # Work with .sde files to overcome password secrecy
str_sde = r"C:\Users\mahvi\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\nis_editor@green3.sde"

 # the Feature Data Set, may be empty if FC's are in the SDE root
str_fds = "Vores_Navne"

 # Search string to find the FC in the str_ws
str_fc = "NamesAtest" 

# Stepwise isolate the FC
arcpy.env.workspace = str_sde
for fds in arcpy.ListDatasets("*", "Feature"):
    print " try fds: "+fds
    if str_fds in fds:
        for fc in fds:
            if str_fc in fc:
                print " * name:" + arcpy.Describe(fc).name

sys.exit()


str_ws = str_sde + str_fds
print "ws: "+str(str_ws)
 
# Set the str_ws for ListFeatureClasses
arcpy.env.str_ws = str_ws
lst_fcs = arcpy.ListFeatureClasses()
print "fcs: "+str(lst_fcs)
 
 
# Set up database connection and edit session
#db_str, db_editSess = SetUpDB(fds)
 
# START AN EDIT SESSION. Must provide the str_ws.
#  http://resources.arcgis.com/en/help/main/10.2/index.html#//018w00000005000000
db_editSess = arcpy.da.Editor(str_sde)
 
# Edit session is started without an undo/redo stack for versioned data
#  (for second argument, use False for unversioned data)
db_editSess.startEditing(False, True)
 
# Start an edit operation
db_editSess.startOperation()
 
 
#for fc in featureclasses:
fc = NIS.DepthsA
 
#arcpy.CalculateField_management(str_ws+fc, GST_LINtxt, "!KMS_LINtxt!", "PYTHON_9.3")
#arcpy.CalculateField_management(str_ws+fc, GST_NID,    "!KMS_NID!", "PYTHON_9.3")
    #with arcpy.da.UpdateCursor(fds+fc, , where_clause="KMS_LINtxt IS NOT NULL OR KMS_NID IS NOT NULL") as uc:
    #    for row in uc:
    #        count += 1
    #        logStr = "Rule {} ({}): updating " .format(rule.id, rule.title)
    #        i = defaultFieldsNum
    #        for i in range(len(rule.fixLst)): # do each of the fixes
    #            logStr += "{} = {} (was {}), ".format(rule.fixLst[i][0], rule.fixLst[i][1], row[defaultFieldsNum+i])
    #            fixVal = rule.fixLst[i][1] # set the update value
    #            row[defaultFieldsNum+i] = fixVal
    #            i += 1
    #        logStr = logStr[0:-2] + " for OBJECTID = {} in {}".format(row[0], fc)
    #        utils.log(logStr)
    #        uc.updateRow(row) # do the actual update
    #        pass
 
 
 
# Stop the edit operation
db_editSess.stopOperation()
 
# Stop the edit session and save the changes
db_editSess.stopEditing(True)
