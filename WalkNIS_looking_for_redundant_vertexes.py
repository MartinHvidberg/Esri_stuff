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
tim_start = datetime.now()    

def points_on_a_line(p):
    #fil_log.write("       poli(): "+str(p)+"\n")
    try:
        if (p[0].X==p[1].X) or (p[1].X==p[2].X): # Identical X, i.e. on a horizontal line. These can give 'division by zero' errors
            if (p[0].X==p[1].X) and (p[1].X==p[2].X): # All are on a line
                #fil_log.write("          poli(): All x on a line ... \n")
                return True
            else:
                #fil_log.write("          poli(): 2, but not 3, x on a line ... "+str(que_points)+"\n")
                return False
        else: # Do the slope method 
            slope12 = 1.0*(p[1].Y-p[0].Y)/(p[1].X-p[0].X)
            slope23 = 1.0*(p[2].Y-p[1].Y)/(p[2].X-p[1].X)
            #fil_log.write("          poli(): slope12: "+str(slope12)+"\n")
            #fil_log.write("          poli(): slope23: "+str(slope23)+"\n")
            return slope12 == slope23
    except:
        fil_log.write("!!! poli(): Exception raised: "+str(p)+"\n")
        return False

def Clean_Vertex_on_a_line(row):
    #fil_log.write("   =row: "+str(row)+"\n")
    geo = row[0] # We just know its the first object in the cursor row, because we made it like that ...
    #fil_log.write("    geo: "+"parts: "+str(geo.partCount)+" points: "+str(geo.pointCount)+" "+"\n")
    #fil_log.write("   JSON: "+geof.JSON+"\n")
    #fil_log.write("    WKT: "+geof.WKT+"\n")
    num_vex = geo.pointCount
    num_rem = 0
    lst_redunts = list()
    if num_vex == 0:
        return (False, "Zero vertexes") # Zero vertex feature makes no sense
    elif num_vex <= 2:
        return (True,geo,num_vex,num_rem) # It takes at least 3 vertexes to have a 'unnecessary' vertex.
    else:
        # Analyze the 'geo' feature
        #fil_log.write("      =geo: "+str(geo)+"\n")
        # walk through 'parts' a.k.a. 'arrays'
        geo_part_n = 0
        for geo_part in geo:
            geo_part_n += 1
            #fil_log.write("      =geo_part : "+str(geo_part)+"\n")
            # walk the individual points in the part/array
            que_points = list()
            for geo_point in geo_part:
                #fil_log.write("       =geo_point : "+str(geo_point)+"\n")
                if len(que_points) < 3: # still filling the que
                    que_points.append(geo_point)
                    
                else: # process a full que, and append the next point
                    # process que
                    if points_on_a_line(que_points):
                        # Make note of point so it can be removed from structure later
                        redunt = que_points[1]
                        lst_redunts.append(redunt)
                        # XXX
                        num_rem += 1
                        fil_log.write("        +++ point : "+str(que_points)+"\n")
                        # remove middel point
                        del que_points[1]
                    else:
                        # remove first (oldest) point
                        del que_points[0]
                    # append next point
                    que_points.append(geo_point)

            return (True,geo,num_vex,num_rem,lst_redunts)


### *** Main *** ###

arcEC.SetMsg("'"+strName+"' ver. "+strVer+" build "+strBuild,0)

# *** Manage input parameters ***
str_deafult_dir = sys.path[0]+"\\".replace("\\\\","\\").replace("\\","/") # OS independent

# ** Harvest strings from GUI       
arcEC.SetMsg("GUI said",0)
str_ws = arcpy.GetParameterAsText(0) # The Feature Dataset
arcEC.SetMsg("Input Workspace: "+str_ws,0)
arcEC.SetMsg("Deaufult directory: "+sys.path[0],0)

# *** Manage output ***
# ** Log file
fil_log = open(str_deafult_dir+u"walkdir.log","w")
fil_log.write("'"+strName+"' ver. "+strVer+" build "+strBuild+"\n")
fil_log.write("Deaufult directory: "+sys.path[0]+"\n")
fil_log.write("Start time: "+str(tim_start)+"\n")
fil_log.write("\n")
# ** Out points file
try:
    fc_out = u"C:\\Martin\\Work\\redundant_vertexes.shp"
    cur_pnt_out = arcpy.da.InsertCursor(fc_out, ["SHAPE@","source"])
except:
    arcEC.SetMsg("Can't find output points file: "+fc_out,2)
    sys.exit(101)

# *** Walk through the 'Work space' ***

feature_classes = []
for dirpath, dirnames, filenames in arcpy.da.Walk(str_ws, datatype="FeatureClass", type=['Polygon', 'Polyline']):
    for filename in filenames:
        arcEC.SetMsg("*** "+str(filename),0)
        if (filename[:4] == "PLTS") or (filename[:8] == "NIS.PLTS"):
            msg = "         Passed (PLTS)"
            fil_log.write("\n*** "+str(filename)+"\n"+msg+"\n")
            arcEC.SetMsg(msg,0)
            pass # Don't process PLTS* feature classes
        elif False: #filename[:15] != "TracksAndRoutes":
            msg = "         Passed (TEST MODE)"
            fil_log.write("\n*** "+str(filename)+"\n"+msg+"\n")
            arcEC.SetMsg(msg,0)
            pass
        elif filename[:4] == "Natu": # These featureclasses tend to be big
            msg = "         Passed (Assumed too big)"
            fil_log.write("\n*** "+str(filename)+"\n"+msg+"\n")
            arcEC.SetMsg(msg,0)
            pass        
        else:
            arcEC.SetMsg("    start "+str(datetime.now()),0)
            fil_log.write("\n*** "+str(filename)+"\n")
            obj_fc = os.path.join(dirpath, filename)
            fil_log.write("    fc : "+str(obj_fc)+"\n")
            # Run through the FC's rows
            with arcpy.da.SearchCursor(obj_fc, ["SHAPE@","OID@"]) as cursor:
                for row in cursor:
                    fil_log.write(" ** oid: "+str(row[1])+"\n")
                    clean = Clean_Vertex_on_a_line(row)
                    if clean[0]:
                        if clean[3] > 0: # removable were found
                            fil_log.write("    cln: --- : "+str(clean[3])+"\n")
                            # insert redundant points in output shapefile
                            for pnt_redunt in clean[4]:
                                cur_pnt_out.insertRow((pnt_redunt,str(filename))) # (the point, the lable)
                            pass
                    else:
                        fil_log.write("   -cln: a 'Geometry object' failed cleaning: "+clean[1]+"\n")
        

# *** All Done - Cleaning up ***

del cur_pnt_out
fil_log.close()

tim_end = datetime.now()
dur_run = tim_end-tim_start
arcEC.SetMsg("Python stript duration (h:mm:ss.dddddd): "+str(dur_run),0)
    
# *** End of Script ***

# Music that accompanied the coding of this script:
#   Donald Fagan - The Nightfly
#   Earth, Wind & Fire - Best of
