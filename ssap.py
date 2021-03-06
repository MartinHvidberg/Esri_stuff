#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Spatial and Structural Analysis Program (SSAP)
Created on 14. August 2014
@author: mahvi@kms.dk / Martin@Hvidberg.net
'''

strName = "SSAP"
strVer = "1.1.0"
strBuild = "'14082291026"

### History
# Ver. 1.0.0 - First working version
# Ver. 1.1.0
#   Introducing filter on PLTS_COMP_SCALE
#   Always filter PLTS* FCs out
#   str_output_dir made a fixed variable

### To do
# Look for XXX in the code

#import sys # for sys.exit()
from datetime import datetime # for datetime.now()
import arcpy
import arcEC # My recycled Easy-arcpy helper functions
import ssap_boxplot

timStart = datetime.now()             
                
def make_fc_statistics(dicIn):
    """ This never really flew ... """
    # Check data and open file...
    try:
        keys1 = dicIn.keys()
        if "FCSs" in keys1:
            keys2 = dicIn["FCSs"].keys()
        else:
            return "Error - No 'FCSs' key found in dic"
    except:
        return "Error - Don't seem to be a dictionary, but a: "+str(type(dicIn))    
    if "fcname" in keys1:
        fn = dicIn["fcname"]
    elif "FCname" in keys1:
        fn = dicIn["FCname"]
    try:
        fil_out = open(str_output_dir + u"SSAP_stat_"+fn+".ect","w")
        fil_out.write("SSAP FC stat: " + fn + "\n") 
    except:
        return "Error - Can't find FCname in dic."
    
    # Write raw data to file
    for k1 in keys1:
        if k1 != "FCSs":
            fil_out.write("X   "+str(k1)+" : "+str(dicIn[k1])+"\n")
    fil_out.write("Y   "+"FCSs : "+str(dicIn["FCSs"].keys())+"\n")
    for k2 in keys2:
        fil_out.write("Z   "+str(k2)+" : "+str(dicIn["FCSs"][k2])+"\n")
    # Make Stat dic
    dic_ssap = dict()
    for k2 in keys2:
        dic_ssap[k2] = dict()
        lstofdic_i = dicIn["FCSs"][k2]
        fil_out.write(" >1> "+str(lstofdic_i)+"\n")
        for dic_i in lstofdic_i:
            for k_i in dic_i.keys():
                if k_i != 'FCSUBTYPE': # No need to save, its redundant to k2
                    if k_i not in dic_ssap[k2]:
                        dic_ssap[k2][k_i] = list()
                    dic_ssap[k2][k_i].append(dic_i[k_i])
        
    # Write stat to file
    fil_out.write(" <2< "+str(dic_ssap)+"\n")
    # Closing
    fil_out.close()
    return 0
    
def make_fc_plotdata(dicIn):
    # Check data and open file...
    try:
        keys1 = dicIn.keys()
        if "FCSs" in keys1:
            keys2 = dicIn["FCSs"].keys()
        else:
            return "Error - No 'FCSs' key found in dic"
    except:
        return "Error - Don't seem to be a dictionary, but a: "+str(type(dicIn))    
    if "fcname" in keys1:
        fn = dicIn["fcname"]
    elif "FCname" in keys1:
        fn = dicIn["FCname"]
    try:
        fil_out = open(str_output_dir + u"SSAP_plot_"+fn+".ect","w")
        fil_out.write("SSAP FC plot : " + fn + "\n") 
    except:
        return "Error - Can't find FCname in dic."
    
    # See what input looks like ... while transforming to Plot suitable data structure
    dic_plotdata = dict() # Data object to be passed to ssap_boxpolt
    dic_plotdata["meta"] = dict() # Dictionary of Meta-data
    dic_plotdata["group"] = dict() # Dictionary with plot data grouped by ...
    dic_plotdata["allio"] = dict() # Dictionary of same plot data, with no grouping, i.e. All-in-one...
    ##fil_out.write("Entire object: "+str(dicIn)+"\n\n")
    for k1 in dicIn.keys():
        if not "FCSs" in k1: # write the meta tags first
            dic_plotdata["meta"][k1] = dicIn[k1]
            ##fil_out.write(" meta: "+str(k1)+" : "+str(dicIn[k1])+"\n")
    for k2 in dicIn["FCSs"].keys():
        ##fil_out.write("  FCS: "+str(k2)+" : "+str(dicIn["FCSs"][k2])+"\n") # These are list objects
        for geoobj in dicIn["FCSs"][k2]:
            ##fil_out.write("  fcs: "+str(k2)+"  geo. "+str(geoobj)+"\n") # These are dict objects
            for para in geoobj.keys():
                if para == "FCSUBTYPE":
                    continue # Redundant to k2, no nead to save ...
                if not para in dic_plotdata["group"].keys():
                    dic_plotdata["group"][para] = dict() # This is the 'parameter' to plot
                if not para in dic_plotdata["allio"].keys():
                    dic_plotdata["allio"][para] = list()
                if "FCSUBTYPE" in geoobj.keys():
                    group = geoobj["FCSUBTYPE"] # Grouping by these groups are the diff between 'group' and 'allio'
                    if group not in dic_plotdata["group"][para].keys():
                        dic_plotdata["group"][para][group] = list() # This the actual list of values for parameter 'para', and in group 'group'
                    # Finally --- Add the actual value
                    dic_plotdata["group"][para][group].append(geoobj[para])
                    dic_plotdata["allio"][para].append(geoobj[para])
                else:
                    arcEC.SetMsg("ERROR : Can't find 'FCSUBTYPE' in this geo-object: "+str(geoobj),2)                
                ##fil_out.write("              > "+str(para)+" : "+str(geoobj[para])+"\n")
                
    # See what the Plot suitable data structure looks like
    fil_out.write("\nNow in PLOT format...\n")
    fil_out.write("The whole lot... "+str(dic_plotdata)+"\n")
    
    obj_meta = dic_plotdata["meta"]
    for tag in obj_meta.keys():
        fil_out.write(" meta  : "+str(tag)+" : "+str(obj_meta[tag])+"\n")
    fil_out.write("       :\n") 
    
    obj_allio = dic_plotdata["allio"]
    for param in obj_allio.keys():
        fil_out.write(" allio : "+str(param)+" : "+str(obj_allio[param])+"\n")
    fil_out.write("       :\n") 
    
    obj_group = dic_plotdata["group"]
    for param in obj_group.keys():
        fil_out.write(" group : "+str(param)+" : \n")
        for grp in obj_group[param].keys():
            fil_out.write(" group :     "+str(grp)+" : "+str(obj_group[param][grp])+"\n")
    
    fil_out.close()
    # Since all is successful, return 0
    return dic_plotdata
    
        
    
# *** Main

arcEC.SetMsg("'"+strName+"' ver. "+strVer+" build "+strBuild,0)

# *** Manage input parameters ***

# ** Harvest strings from GUI       
arcEC.SetMsg("GUI said",0)
strFDS = arcpy.GetParameterAsText(0) # The Feature Dataset
strWHR = arcpy.GetParameterAsText(1) # The where clause
arcEC.SetMsg("Input Feature dataset: "+strFDS +", "+strWHR,0)

# *** Open output files
str_output_dir = u"C:\Martin\Work\ssap\\"
# ** Log file
fil_log = open(str_output_dir + u"ssap.log","w")
fil_log.write("'"+strName+"' ver. "+strVer+" build "+strBuild+"\n")
fil_log.write(str(timStart)+"\n")
fil_log.write("\n")

# *** Open Descriptions ***
 
arcEC.SetMsg("Open Description",0)
dicDescribtion = arcpy.Describe(strFDS)
 
strReport  = ""
strReport += "\n   - catalog path: " + dicDescribtion.catalogPath
strReport += "\n   - name: " + dicDescribtion.name
strReport += "\n   - data type: " + dicDescribtion.dataType
strReport += "\n   - children expanded: " + str(dicDescribtion.childrenExpanded)
strReport += "\n   - children count: " + str(len(dicDescribtion.children))
arcEC.SetMsg(strReport,0)
 
if len(dicDescribtion.children) > 0:
    arcEC.SetMsg("   Analyzing Descriptions of layers: "+str(len(dicDescribtion.children)),0)
    numFCcounter = 0
    for dicChildDescribtion in dicDescribtion.children:
        numFCcounter += 1    
        arcEC.SetMsg("\n   FC Count : " + str(numFCcounter) + " of " + str(len(dicDescribtion.children)),0)
        arcEC.SetMsg("      - name: " + dicChildDescribtion.name,0)
        if (dicChildDescribtion.name[-1:] != "P") and (not "PLTS" in dicChildDescribtion.name): # and (dicChildDescribtion.name in ["OffshoreInstallationsL","RegulatedAreasAndLimitsA","NIS.OffshoreInstallationsL","NIS.RegulatedAreasAndLimitsA"]):
            if dicChildDescribtion.dataType == "FeatureClass":
                arcEC.SetMsg("         > data type: " + dicChildDescribtion.dataType,0)
                lstFields = dicChildDescribtion.fields
                # Compile list of fields we like
                lst_fields_wl = list()
                lst_fields_wl.append("SHAPE@")
                lstGoodNames = ["FCSUBTYPE","SHAPE_Length","SHAPE.LEN","SHAPE_Area","SHAPE.AREA"]
                for fldG in lstFields:
                    if fldG.name in lstGoodNames:
                        fil_log.write("         * "+fldG.type+" : "+fldG.name+"\n")
                        lst_fields_wl.append(fldG.name)
                    else:
                        pass
                        #fil_log.write("         % "+fldG.type+" : "+fldG.name+"\n")
                # Keeper of everything about the FC, by FCS, incl. fields        
                dicFC = dict()
                dicFC["FCname"] = dicChildDescribtion.name
                dicFC["fldswl"] = lst_fields_wl
                del lst_fields_wl, fldG, lstGoodNames, lstFields
                pos = dicChildDescribtion.name.find(".") # in SDE name is 'NIS.Blablabla', we just want Blablabla.
                if pos >= 0:
                    strNameWithoutPrefix = dicChildDescribtion.name[pos+1:]
                else:
                    strNameWithoutPrefix = dicChildDescribtion.name
                dicFC["fcname"] = strNameWithoutPrefix
                dicFC["FCSs"] = dict()
                # Cursor ...
                str_where = "PLTS_COMP_SCALE < 3000000"
                arcEC.SetMsg("      - curN: " + dicChildDescribtion.catalogPath+" : "+str(dicFC["fldswl"]),0)                
                with arcpy.da.SearchCursor(dicChildDescribtion.catalogPath, dicFC["fldswl"], str_where) as cur:
                    for row in cur:
                        try:
                            #Extract the attributes from this row
                            dic_att = dict()
                            for fld_i in range(len(dicFC["fldswl"])):
                                if fld_i == 0: # first is always SHAPE@
                                    dic_att["NS"] = row[0].extent.height
                                    dic_att["EW"] = row[0].extent.width
                                    dic_att["NSEWarea"] = row[0].extent.height * row[0].extent.width
                                    dic_att["hullarea"] = row[0].convexHull().area
                                    dic_att["pointcnt"] = row[0].pointCount
                                else:
                                    dic_att[str(dicFC["fldswl"][fld_i])] = row[fld_i]
                            # Add dic_att to dicFC
                            # Check if this is a new FSC, then make a dic for it ...
                            strFCS = dic_att["FCSUBTYPE"]
                            if strFCS not in dicFC["FCSs"].keys():
                                dicFC["FCSs"][strFCS] = list()
                            dicFC["FCSs"][strFCS].append(dic_att)
                            del dic_att
                        except:
                            fil_log.write("Exception raised at row: "+str(row)+"\n")
                # Post traveling rows
                bol_statistics = False
                bol_plot = True
                if bol_statistics:
                    obj_stat = make_fc_statistics(dicFC)
                    if obj_stat != 0:
                        arcEC.SetMsg(" !!! Problem with generating a Statisitcal_object: "+obj_stat,1)
                if bol_plot:
                    obj_plot = make_fc_plotdata(dicFC) 
                    ssap_boxplot.pltit(obj_plot)
                    arcEC.SetMsg("   pltit() done ...",0)
                    
                # Cleaning variables
                del dicFC
                
            else:
                arcEC.SetMsg(" !!! Not a Feature Class: "+dicChildDescribtion.dataType,1)
else:
    arcEC.SetMsg("No Feature Layers found",1)

# *** All Done - Cleaning up ***

fil_log.close()
timEnd = datetime.now()
durRun = timEnd-timStart
arcEC.SetMsg("Python stript duration (h:mm:ss.dddddd): "+str(durRun),0)
    
# *** End of Script ***

# Music that accompanied the coding of this script:
#   Donald Fagan - The Nightfly
#   Earth, Wind & Fire - Best of