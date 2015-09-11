#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import arcpy

## Version 1.11 '150831/MaHvi

def SetMsg(msg, severity=0, fil_log=False): # 0:Message, 1:Warning, 2:Error
    try:
        print msg
        for string in msg.split('\n'):
            string = ":) "+string
            if severity == 0:
                arcpy.AddMessage(string)
            elif severity == 1:
                arcpy.AddWarning(string)
            elif severity == 2:
                arcpy.AddError(string)
    except:
        pass
    try:
        fil_log.write(string+"\n")
    except:
        pass
    
def ecMessage(strI,numI=0,severity=0):
    """ Neither message number nor severity is mandatory """
    if numI == 0:
        SetMsg("   Message: "+strI,0)
    else:
        SetMsg("   Message: "+str(numI)+" : "+strI,0)
    
def ecWarning(strI,numI,severity=0):
    """ Severity is not mandatory """
    SetMsg(" ! Warning: "+str(numI)+" : "+strI,1)
    
def ecError(strI,numI,severity):
    """ Severity > 0 causes program termination """
    SetMsg("!!!Error: "+str(numI)+" : "+strI,2)
    if severity > 0:
        sys.exit(numI)
    
def Describe2String(desIn):
    strReport = ""
    if hasattr(desIn, "Name"):
        strReport +="\n Name: "+desIn.Name
    if hasattr(desIn, "baseName"):
        strReport +="\n baseName: "+desIn.baseName
    if hasattr(desIn, "dataType"):
        strReport +="\n dataType: "+desIn.dataType 
    #if hasattr(desIn, "dataElementType"):
    #    strReport +="\n dataElementType: "+desIn.dataElementType
    if hasattr(desIn, "catalogPath"):
        strReport +="\n catalogPath: "+desIn.catalogPath
    if hasattr(desIn, "children"):
        strReport +="\n children: "+str(len(desIn.children))
    if hasattr(desIn, "fields"):
        strReport +="\n fields: "+str(len(desIn.fields))
        if len(desIn.fields) > 0:
            for fldX in desIn.fields:
                strReport +="\n  field: "+fldX.name
    if hasattr(desIn, "pludder"):
        strReport +="\n pludder: "+desIn.pludder
    return strReport

def Table2Ascii(tblIn):
    strReport = ""
    desIn = arcpy.Describe(tblIn)
    if hasattr(desIn, "dataType"):
        if desIn.dataType == "Table":
            strReport +="\n Table2Ascii ::"
            if hasattr(desIn, "fields"):
                strReport +="\n  fields: "+str(len(desIn.fields))+"\n"
                if len(desIn.fields) > 0:
                    for fldX in desIn.fields:
                        strReport +="|"+fldX.name+" <"+fldX.type+">"
                    rows = arcpy.SearchCursor(tblIn)
                    numRows = 0
                    for rowX in rows:
                        strReport += "\n  "
                        for fldX in desIn.fields:
                            strReport += "|"+str(rowX.getValue(fldX.name))
                        numRows += 1
                    strReport += "\n  Row count: "+str(numRows)
            else:
            	strReport +="No Fields in tabel ..."
    return strReport

def Table2Ascii_byFields(tblIn):
    strReport = ""
    desIn = arcpy.Describe(tblIn)
    if hasattr(desIn, "dataType"):
        if desIn.dataType == "Table":
            strReport +="Table2Ascii_ByFields"
            if hasattr(desIn, "fields"):
                strReport +="\n  fields: "+str(len(desIn.fields))
                if len(desIn.fields) > 0:
                    for fldX in desIn.fields:
                        rows = arcpy.SearchCursor(tblIn)
                        strReport +="\n  field: "+fldX.name+" <"+fldX.type+">"
                        strReport += "\n  "
                        for rowX in rows:
                            strReport += "|"+str(rowX.getValue(fldX.name))
                        rows.reset()
    return strReport

def Dict2String(dicIn):
    strReport = ""
    lstK = dicIn.keys()
    lstK.sort()
    for K in lstK:
        strReport += str(K)+" : "+str(dicIn[K])+"\n"
    return strReport

def is_FC_editable(FC):
    """ Only if the FC is in a Edit session can we work with multiple Update cursors on it """
    try:
        upCursor1 = arcpy.da.UpdateCursor(FC,'*')
        upCursor2 = arcpy.da.UpdateCursor(FC,'OBJECTID')
        with upCursor2 as cursor:
            for row in cursor:
                pass    
        return True
    except:
        return False

def encodeIfUnicode(strval):
    """Encode if string is unicode."""
    if isinstance(strval, unicode):
        return strval.encode('ISO-8859-1')
    return str(strval)

def encodeIfUnicodeAndaoe(strval):
    """Encode if string is unicode."""
    if isinstance(strval, unicode):
        return strval.encode('ISO-8859-1').replace('\xe6','ae').replace('\xf8','oe').replace('\xe5','aa').replace('\xd8','OE')
    return str(strval)

def find_ws(path, ws_type=''):
    """finds a valid workspace path for an arcpy.da.Editor() Session

    Required:
        path -- path to features or workspace

    Optional:
        ws_type -- option to find specific workspace type (FileSystem|LocalDatabase|RemoteDatabase)

    """
    # try original path first
    if os.sep not in path:
        path = arcpy.Describe(path).catalogPath
    desc = arcpy.Describe(path)
    if hasattr(desc, 'workspaceType'):
        if ws_type and ws_type == desc.workspaceType:
            return path
        elif not ws_type:
            return path

    # search until finding a valid workspace
    SPLIT = filter(None, path.split(os.sep))
    if path.startswith('\\\\'):
        SPLIT[0] = r'\\{0}'.format(SPLIT[0])

    # find valid workspace
    for i in xrange(1, len(SPLIT)):
        sub_dir = os.sep.join(SPLIT[:-i])
        desc = arcpy.Describe(sub_dir)
        if hasattr(desc, 'workspaceType'):
            if ws_type and ws_type == desc.workspaceType:
                return sub_dir
            elif not ws_type:
                return sub_dir

class ECUpdateCursor(object):
    """wrapper class for arcpy.da.UpdateCursor, to automatically
    implement editing (required for versioned data, and data with
    geometric networks, topologies, network datasets, and relationship
    classes"""
    def __init__(self, *args, **kwargs):
        """initiate wrapper class for update cursor.  Supported args:

        in_table, field_names, where_clause=None, spatial_reference=None,
        explode_to_points=False, sql_clause=(None, None)
        """
        self.args = args
        self.kwargs = kwargs
        self.edit = None

    def __enter__(self):
        ws = None
        if self.args:
            ws = find_ws(self.args[0])
        elif 'in_table' in self.kwargs:
            ws = find_ws(self.kwargs['in_table'])
        self.edit = arcpy.da.Editor(ws)
        self.edit.startEditing()
        self.edit.startOperation()
        return arcpy.da.UpdateCursor(*self.args, **self.kwargs)

    def __exit__(self, type, value, traceback):
        self.edit.stopOperation()
        self.edit.stopEditing(True)
        self.edit = None

# Music that accompanied the coding of this script:
#   Deep Forest - Savana Dance
