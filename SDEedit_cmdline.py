# This module is to be called from command line mode


### from http://gis.stackexchange.com/questions/119938/error-with-da-updatecursor-and-sde-feature-classes


#Locals
strFCname = r"PPGIS.Strux\PPGIS.Land_Projects_Parcels_P6"
Parent = "SDE.DEFAULT"
version = "SDE_Test"
#Server = ***
#Service = ***
user = "mahvi"
#Pass = ***
SDE = "Database Connections\PipelinePathways.sde"
temploc = r"C:\Martin\Work"
fil = "SDETempConn"

env.overwriteOutput = True

#Create Version
print "Creating version"
CreateVersion_management (SDE, Parent, version, "PUBLIC")
VersionName = user.lower() + "_" + version

#Create new connection
workspace = os.path.join (temploc, fil + ".sde")
print "Creating SDE connection"
CreateArcSDEConnectionFile_management (temploc, fil, Server, Service, username = user, password = Pass, version = VersionName)

#Layers
FC = os.path.join (workspace, strFCname)
MakeFeatureLayer_management (FC, "MyLyr")

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
ChangeVersion_management("MyLyr", "TRANSACTIONAL", Parent)

#Reconcile and post
print "Reconciling and posting"
ReconcileVersions_management (workspace, "", Parent, VersionName, with_post = "POST", with_delete = "DELETE_VERSION")

 