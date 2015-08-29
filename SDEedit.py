#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
SDE edit - makes, and saves an edit in a versioned SDE db
Created on 29. August 2015
@author: mahvi@kms.dk / Martin@Hvidberg.net
'''

strName = "SDE edit"
strVer = "1.0.0"
strBuild = "'150829xxxx"

### History
# Ver. 1.0.0 - First working version

### To do
# Look for XXX in the code

#import sys
#import os
from datetime import datetime # for datetime.now()
import arcpy
#import arcEC # My recycled Easy-arcpy helper functions
tim_start = datetime.datetime.now()

### from http://gis.stackexchange.com/questions/119938/error-with-da-updatecursor-and-sde-feature-classes

import os
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

 