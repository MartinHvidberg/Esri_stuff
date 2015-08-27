#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Walk the NIS
Created on 29. August 2014
@author: mahvi@kms.dk / Martin@Hvidberg.net
'''

strName = "WalkNIS"
strVer = "1.0.0"
strBuild = "'140830xxxx"

### History
# Ver. 1.0.0 - First working version

### To do
# Look for XXX in the code

import sys
import os
from datetime import datetime # for datetime.now()
import arcpy
import arcEC # My recycled Easy-arcpy helper functions
tim_start = datetime.datetime.now() 

def Main(str_ws, str_logfile=""):
    
    # ** Log file
    if str_logfile != "":
        try:
            fil_log = open(str_deafult_dir+str_logfile,"w")
            fil_log.write("'"+strName+"' ver. "+strVer+" build "+strBuild+"\n")
            fil_log.write("Deaufult directory: "+sys.path[0]+"\n")
            fil_log.write("Start time: "+str(tim_start)+"\n")
            fil_log.write("\n")
        except:
            arcEC.SetMsg("Error opening Log file",1)
            sys.exit(102)
    
    # *** Walk through the 'Work space' ***

    msg = "Walking: "+str_ws
    fil_log.write("\n*** "+msg+"\n")
    arcEC.SetMsg(msg,0)
    
    for dirpath, dirnames, filenames in arcpy.da.Walk(str_ws, datatype="FeatureClass"):
        for filename in filenames:
            arcEC.SetMsg("*** "+str(filename),0)
            if (filename[:4] == "PLTS") or (filename[:8] == "NIS.PLTS"):
                msg = "         Passed (PLTS)"
                fil_log.write("\n*** "+str(filename)+"\n"+msg+"\n")
                arcEC.SetMsg(msg,0)
                pass # Don't process PLTS* feature classes
            
            else:
                arcEC.SetMsg("    start "+str(datetime.datetime.now()),0)
                fil_log.write("\n*** "+str(filename)+"\n")
                obj_fc = os.path.join(dirpath, filename)
                fil_log.write("    fc : "+str(obj_fc)+"\n")
                # Run through the FC's rows
                with arcpy.da.SearchCursor(obj_fc, ["SHAPE@","OID@"]) as cursor:
                    for row in cursor:
                        fil_log.write(" ** oid: "+str(row[1])+"\n")
    
    # *** All Done - Cleaning up ***
    
    try:
        fil_log.write(result+"\n")
        fil_log.close()
    except:
        pass

if __name__ == "__main__":
       
    arcEC.SetMsg("'"+strName+"' ver. "+strVer+" build "+strBuild,0)
    
    # *** Manage input parameters ***
    str_deafult_dir = sys.path[0]+"\\".replace("\\\\","\\").replace("\\","/") # OS independent
    
    # ** Harvest strings from GUI       
    arcEC.SetMsg("GUI said",0)
    str_ws = arcpy.GetParameterAsText(0) # The Feature Dataset
    str_ws = "C:/Users/b004218/AppData/Roaming/ESRI/Desktop10.3/ArcCatalog/EC_nis_editor@green3.sde/NIS.Nautical" # The Feature Dataset
    str_lf =  "NISwalk.ecl" # a log file
    
    # ** Show input parameters
    arcEC.SetMsg("Input Workspace: "+str_ws,0)
    arcEC.SetMsg("Log file: "+str_lf,0)
    arcEC.SetMsg("Deaufult directory: "+sys.path[0],0)
    
    # ** Run Main program wiht these parameters ...
    result = Main(str_ws,str_lf)

tim_end = datetime.datetime.now()
dur_run = tim_end-tim_start
arcEC.SetMsg("Python stript duration (h:mm:ss.dddddd): "+str(dur_run),0)
    
# *** End of Script ***

# Music that accompanied the coding of this script:
#   Donald Fagan - The Nightfly
#   Earth, Wind & Fire - Best of