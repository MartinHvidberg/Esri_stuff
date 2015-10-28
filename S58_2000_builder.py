def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
#['ACHARE', 'ACHBRT', 'ADMARE', 'AIRARE', 'BCNCAR', 'BCNISD', 'BCNLAT', 'BCNSAW', 'BCNSPP', 'BERTHS', 'BOYCAR', 'BOYINB', 'BOYISD', 'BOYLAT', 'BOYSAW', 'BOYSPP', 'BRIDGE', 'BUAARE', 'BUISGL', 'CANALS', 'CAUSWY', 'CBLARE', 'CBLOHD', 'CBLSUB', 'CGUSTA', 'CHKPNT', 'COALNE', 'CONVYR', 'CONZNE', 'CRANES', 'CTRPNT', 'CTSARE', 'DAMCON', 'DAYMAR', 'DEPARE', 'DISMAR', 'DMPGRD', 'DOCARE', 'DRGARE', 'DRYDOC', 'DWRTCL', 'DWRTPT', 'DYKCON', 'FAIRWY', 'FERYRT', 'FLODOC', 'FNCLNE', 'FOGSIG', 'FORSTC', 'FRPARE', 'FSHFAC', 'FSHGRD', 'FSHZNE', 'GATCON', 'GRIDRN', 'HRBARE', 'HRBFAC', 'HULKES', 'ICEARE', 'ICNARE', 'ISTZNE', 'LIGHTS', 'LITFLT', 'LITVES', 'LNDARE', 'LNDELV', 'LNDMRK', 'LNDRGN', 'LOGPON', 'LOKBSN', 'MARCUL', 'MIPARE', 'MORFAC', 'M_COVR', 'M_HOPA', 'M_NSYS', 'M_QUAL', 'M_SDAT', 'M_SREL', 'M_VDAT', 'NAVLNE', 'NEWOBJ', 'OBSTRN', 'OFSPLF', 'OILBAR', 'OSPARE', 'PILBOP', 'PILPNT', 'PIPARE', 'PIPOHD', 'PIPSOL', 'PONTON', 'PRCARE', 'PRDARE', 'PYLONS', 'RADLNE', 'RADRFL', 'RADRNG', 'RADSTA', 'RAILWY', 'RCRTCL', 'RCTLPT', 'RDOCAL', 'RDOSTA', 'RECTRC', 'RESARE', 'RETRFL', 'RIVERS', 'ROADWY', 'RSCSTA', 'RTPBCN', 'RUNWAY', 'SBDARE', 'SEAARE', 'SILTNK', 'SISTAT', 'SISTAW', 'SLCONS', 'SLOGRD', 'SLOTOP', 'SMCFAC', 'SOUNDG', 'SPLARE', 'SUBTLN', 'SWPARE', 'TESARE', 'TOPMAR', 'TSELNE', 'TSEZNE', 'TSSBND', 'TSSCRS', 'TSSLPT', 'TSSRON', 'TS_FEB', 'TS_PNH', 'TS_PRH', 'TS_TIS', 'TUNNEL', 'TWRTPT', 'T_HMON', 'T_NHMN', 'T_TIMS', 'UWTROC', 'VEGATN', 'WATFAL', 'WATTUR', 'WEDKLP', 'WRECKS']
#['BCNSHP', 'BOYSHP', 'BUISHP', 'CATACH', 'CATAIR', 'CATBRG', 'CATBUA', 'CATCAM', 'CATCAN', 'CATCBL', 'CATCHP', 'CATCOA', 'CATCON', 'CATCOV', 'CATCRN', 'CATCTR', 'CATDAM', 'CATDIS', 'CATDOC', 'CATDPG', 'CATFIF', 'CATFNC', 'CATFOG', 'CATFOR', 'CATFRY', 'CATGAT', 'CATHAF', 'CATHLK', 'CATICE', 'CATINB', 'CATLAM', 'CATLIT', 'CATLMK', 'CATLND', 'CATMFA', 'CATMOR', 'CATMPA', 'CATNAV', 'CATOBS', 'CATOFP', 'CATOLB', 'CATPIL', 'CATPIP', 'CATPLE', 'CATPRA', 'CATPYL', 'CATRAS', 'CATREA', 'CATROD', 'CATROS', 'CATRSC', 'CATRTB', 'CATRUN', 'CATSCF', 'CATSEA', 'CATSIL', 'CATSIT', 'CATSIW', 'CATSLC', 'CATSLO', 'CATSPM', 'CATTRK', 'CATTSS', 'CATVEG', 'CATWAT', 'CATWED', 'CATWRK', 'CATZOC', 'CAT_TS', 'COLOUR', 'COLPAT', 'CONDTN', 'CONRAD', 'CONVIS', 'EXCLIT', 'EXPSOU', 'FUNCTN', 'HORDAT', 'JRSDTN', 'LITCHR', 'LITVIS', 'MARSYS', 'NATCON', 'NATQUA', 'NATSUR', 'PRODCT', 'QUAPOS', 'QUASOU', 'RESTRN', 'SIGGEN', 'STATUS', 'SURTYP', 'TECSOU', 'TOPSHP', 'TRAFIC', 'T_ACWL', 'T_MTOD', 'VERDAT', 'WATLEV']


bol_act = False # To act on this input line
lst_att = list()
lst_obt = list()
dic_col = dict()

with open("S-58_2000_raw.txt") as f:
    for line in f:
        #print "    "+line.strip()
        if bol_act:
            lst_l = line.strip().split()
            if len(lst_l) == 2: # Its an Attribute
                str_att = lst_l[0]
                lst_att.append(str_att)
                #print "Att.="+str_att
            elif len(lst_l) > 2: # It must be a ObjType
                str_obt = lst_l[0]
                lst_obt.append(str_obt)
                # Test cases
                lst_tcs = list()
                bol_test = False
                if str_obt == 'BUISGL' and str_att == 'COLOUR':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" * << Anything goes ..."
                    
                if str_obt == 'BOYSPP' and str_att == 'COLOUR':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" * # << Anything colour, but must have colour"
                    
                if str_obt == 'M_QUAL' and str_att == 'CATZOC':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" * (#) << Anything value, but must have value, and can't be unknown"
                    
                if str_obt == 'LIGHTS' and str_att == 'COLOUR':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" Numbers and # together << Mandetory, with colour restrictions"
                    
                if str_obt == 'FAIRWY' and str_att == 'RESTRN':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" many valus"
                    
                if str_obt == 'T_HMON' and str_att == 'T_MTOD':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" complex"
                    
                if str_obt == 'BRIDGE' and str_att == 'CONDTN':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" Numbers << Value restrictions"
                    
                if str_obt == 'CBLOHD' and str_att == 'CONDTN':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" Polluted info"
                    
                if str_obt == 'MORFAC' and str_att == 'WATLEV':
                    bol_test = True
                    print "\nTest case "+str_obt+" "+str_att+" Obsolete values"
                    
                # ------
                if bol_test: print "raw: "+line.strip()
                if not str_obt in dic_col.keys(): # Make ObjType
                    dic_col[str_obt] = dict()
                if not str_att in dic_col[str_obt].keys(): # Make Attrib
                    dic_col[str_obt][str_att] = dict()
                if bol_test: print "[2]: "+str(lst_l[2])
                if (RepresentsInt(lst_l[2])) or ("-" in lst_l[2]):
                    dic_col[str_obt][str_att]['Allow'] = lst_l[2].split('-') # Add Allowed
                if ("#" in line):
                    dic_col[str_obt][str_att]['Manda'] = True # Add Allowed
                if ("(#)" in line):
                    dic_col[str_obt][str_att]['Unknw'] = False # Add Allowed
                if bol_test: print "dic: "+str(dic_col[str_obt][str_att])
        if "====== Start from here =====" in line:
            bol_act = True

# Print out
if False:
    lst_obt = list(set(lst_obt))
    lst_obt.sort()
    lst_att = list(set(lst_att))
    lst_att.sort()
    for obt in lst_obt:
        for att in lst_att:
            if att in dic_col[obt]:
                if 'Manda' in dic_col[obt][att]:
                    print obt+" : "+att+" : Mandatory "+str(dic_col[obt][att]['Manda'])
                if 'Allow' in dic_col[obt][att]:
                    print obt+" : "+att+" : "+str(dic_col[obt][att]['Allow'])

    print lst_obt
    print lst_att