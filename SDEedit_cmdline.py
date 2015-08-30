# This module is to be called from command line mode

import arcpy

### from http://gis.stackexchange.com/questions/119938/error-with-da-updatecursor-and-sde-feature-classes

#Locals
SDE = "C:\Users\mahvi\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\nis_editor@green3.sde"
Parent = "SDE.DEFAULT"
version = "SDE_Test"
strFCname = r"NIS.Vores_Navne\GNDBtest"
#Server = ***
#Service = ***
user = "mahvi"
#Pass = ***
temploc = r"C:\Martin\Work"
fil = "SDEtempConn"

arcpy.env.overwriteOutput = True

#Create Version
print "Creating version"
arcpy.CreateVersion_management(SDE, Parent, version, "PUBLIC")
VersionName = user.lower() + "_" + version

#Create new connection
workspace = os.path.join (temploc, fil + ".sde")
print "Creating SDE connection"
arcpy.CreateArcSDEConnectionFile_management(temploc, fil, Server, Service, username = user, password = Pass, version = VersionName)

#Layers
FC = os.path.join (workspace, strFCname)
arcpy.MakeFeatureLayer_management(FC, "MyLyr")

#Start editing
print "Initiating editing"
edit = arcpy.da.Editor(workspace)
edit.startEditing()
edit.startOperation()

#Test Cursor
print "Testing cursor"
cur_my = da.UpdateCursor ("MyLyr", ["NAME"])
for row in cur_my:
    print row[0]
del row
del cur_my

#Stop/save edits
edit.stopOperation()
print "Stopping editing"
edit.stopEditing("True")

#Switch to version
print "Switching version"
arcpy.ChangeVersion_management("MyLyr", "TRANSACTIONAL", Parent)

#Reconcile and post
print "Reconciling and posting"
arcpy.ReconcileVersions_management (workspace, "", Parent, VersionName, with_post = "POST", with_delete = "DELETE_VERSION")

 