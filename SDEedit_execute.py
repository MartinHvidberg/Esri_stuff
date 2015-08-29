#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
SDE edit - makes, and saves an edit in a versioned SDE db
This module is the generic SDE Edit module
It should not be run directely, but from another script (command line script, GUI script or .pyt script)
-> Assuming all ready in en edit version <-
Created on 29. August 2015
@author: mahvi@kms.dk / Martin@Hvidberg.net
'''

strName = "SDE edit"
strVer = "0.1.0"
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
