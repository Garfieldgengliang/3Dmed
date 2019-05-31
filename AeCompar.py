# -*- coding: utf-8 -*-
"""
Comparision -- compare the calculated as with real value

@author: gengliang.li
"""

from DbConnection import DbConnection

from Dbinfo import Dbinfo

from contextlib import closing

import sys

import datetime


class AeCompar:
    
    
    def __init__(self, fileName):
        
        self.fileName = fileName
        
        Dbconnection = DbConnection(self.fileName)
        self.connection = Dbconnection.connectDb()
        
    # this function is to select all the tuples in crim_e_ae ( please pay attention to "all the tuples" )
    # that has ae name in cc_dict_ae, preparing for grade check  
    def aeReal(self):
        
        with closing(self.connection.cursor()) as cur:
            
            sqlstring =  "select name from cc_dict_ae "          
            cur.execute(sqlstring)          
            targettable = cur.fetchall()
        
        aelist = []        
        for item in targettable:
            aelist.append(item[0]) # select all the ae names and store them in a list
            
        Dbinformation = Dbinfo(self.connection)
        aliadic = Dbinformation.ctcaeAliaTable() # get alias dictionary in case aeterm appears as its alia form
            
        with closing(self.connection.cursor()) as cur:
            
            sqlstring =  "select subj_3d_id, aespid, ae, aeterm, aestdat, aeendat, aetoxgr from crim_e_ae "            
            cur.execute(sqlstring)            
            targetraw = cur.fetchall() # get all the potentially useful information from crim_e_ae 
        
        targetlist = []
        for item in targetraw:
            if item[2] in aelist:
                newlist = [item[0]]+[item[1]]+[item[2]]+[item[4]]+[item[5]]+[item[6]]
                targetlist.append(newlist)
            
            elif item[3] in aelist:
                newlist = [item[0]]+[item[1]]+[item[3]]+[item[4]]+[item[5]]+[item[6]]
                targetlist.append(newlist)  
            
            elif item[2] in aliadic.keys():
                newlist = [item[0]]+[item[1]]+[aliadic[item[2]]]+[item[4]]+[item[5]]+[item[6]]
            
            elif item[3] in aliadic.keys():
                newlist = [item[0]]+[item[1]]+[aliadic[item[3]]]+[item[4]]+[item[5]]+[item[6]]

            # if ae or aeterm in the ae list, then select this tuple and store it in a list    
            
        for item in targetlist:
            
            if item[3]:
                
                if item[4]:
                    
                    startdate = item[3]
                    enddate = item[4]
                    delta = datetime.timedelta(days=1)
                    
                    aelabstdate = startdate - delta
                    aelabendate = enddate + delta
            
                    item.append(aelabstdate)  
                    item.append(aelabendate) 
                    
                else:
                    
                    startdate = item[3]
                    delta = datetime.timedelta(days=1)
                    
                    aelabstdate = startdate - delta
                    aelabendate = startdate + delta
                    
                    item.append(aelabstdate)  
                    item.append(aelabendate)
            else:
                sys.exit()
            
            
        return targetlist # the structute of item in this list is
                    # [[subj_3d_id],[aespid],[aeName],[aestartdate],[aeenddate],[originalgrade],[labcheckstdate],[labcheckenddate]]
        
        
        
        
        







