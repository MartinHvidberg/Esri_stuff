#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Walk the NamesA and look for potential redundant Names
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

def lookInto(dic_samename, strN, fil_log):
    lst_keyT = dic_samename.keys()
    if len(lst_keyT) > 1:
        lst_keyT.sort()
        fil_log.write(strN +" - KeyTypes: "+str(lst_keyT)+"\n")
        # If one of the nametypes are unknown
        if '0' in lst_keyT:
            pass # code later ...
        # Deal with same name and same type duplicates
        for strT in lst_keyT:
            lst_itms = dic_samename[strT]
            if len(lst_itms) > 1:
                fil_log.write(" * " + strN + " / " + str(strT) + " = " + str(lst_itms) + "\n")
    return

def totalCount(dic_samename):
    numC = 0
    for keyT in dic_samename.keys():
        for keyO in dic_samename[keyT]:
            numC += 1
    return numC

def makeGroups(dic_samename, numDist):
    return [1,2,3,4]

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
            
            if not ("NamesA" in filename):
                msg = "         Passed (All but NamesA)"
                fil_log.write("\n*** "+str(filename)+"\n"+msg+"\n")
                arcEC.SetMsg(msg,0)
                pass # Don't process PLTS* feature classes
                
            else:
                arcEC.SetMsg("    start "+str(datetime.datetime.now()),0)
                fil_log.write("\n*** "+str(filename)+"\n")
                obj_fc = os.path.join(dirpath, filename)
                fil_log.write("    fc : "+str(obj_fc)+"\n")
                # List the fields
                lst_field_names = [f.name for f in arcpy.ListFields(obj_fc)]
                fil_log.write("    Fields: "+str(lst_field_names)+"\n")
                # Run through the FC's rows
                dic_NamGL = dict()
                with arcpy.da.SearchCursor(obj_fc, ["SHAPE@","OID@","OBJNAM","NAMETYPE"]) as cursor:
                    for row in cursor:
                        int_oid = row[1]
                        str_objnam = arcEC.encodeIfUnicodeAndaoe(row[2])
                        int_nametype = row[3]
                        try:
                            if not str(str_objnam) in dic_NamGL.keys(): # never seen name before
                                dic_NamGL[str(str_objnam)] = dict()
                            if not str(int_nametype) in dic_NamGL[str(str_objnam)]: # never seen that name, of that nametype, before
                                dic_NamGL[str(str_objnam)][str(int_nametype)] = list()
                            dic_NamGL[str(str_objnam)][str(int_nametype)].append(str(int_oid))
                        except UnicodeEncodeError as e:
                            str_error = "    ERROR: "+e.message+"\nOID: "+str(int_oid)+"\nOBJNAM: "+str_objnam+"\nNAMETYPE: "+str(int_nametype)+"\n"
                            arcEC.SetMsg(str_error,2)
                            fil_log.write(str_error)
                        
    # *** Analyse th collected info
    fil_log.write("\n*** Analysing results\n")
    lst_duplicates = list()
    lst_keyN = dic_NamGL.keys()
    lst_keyN.sort()
    #fil_log.write("KeyNames: "+str(lst_keyN)+"\n")
    for strN in lst_keyN:
        dic_samename = dic_NamGL[strN]
        ###
        #lookInto(dic_samename, strN, fil_log)
        numTC = totalCount(dic_samename)
        if numTC > 1:
            fil_log.write(strN + " : "+ str(numTC))
            lst_grps = makeGroups(dic_samename, 10)
            fil_log.write(" g "+ str(len(lst_grps)) + "\n")
        ###
                                
    
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
    str_ws = "C:/Users/b004218/AppData/Roaming/ESRI/Desktop10.3/ArcCatalog/EC_nis_editor@green3.sde/NIS.Vores_Navne" # The Feature Dataset
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
