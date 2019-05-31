# -*- coding: utf-8 -*-
"""
Lrinfo - get lab information given a subjectID, a RecordNum and a ae name

@author: gengliang.li
"""
from CTCAEinfo import CTCAEinfo

from contextlib import closing

class Lrinfo:
    
    def __init__(self, connection, subj_3d_id, startdate, enddate, rules, para, alias, units, aeName):
        
        self.connection = connection
        
        self.subj_3d_id = subj_3d_id
        self.startdate = startdate
        self.enddate = enddate
        
        self.rules = rules
        self.para = para
        self.units = units
        self.alias = alias
        
        self.aeName = aeName
     
    # this function is to find the target parameter given an ae name    
    def findPara(self):
        
        inforCatch = CTCAEinfo(self.connection, self.rules, self.para, self.units, self.aeName)
        
        parameter = inforCatch.aeParaInfo()
        
        return parameter # a list of parameter(s) , like ['hemoglobin']
    
    # this function is to return the parameter value dictionary given ProjectID, subjectId and Record number
    def valueLlnUlnUnitInfo(self): 
        
        valuedic = {}
        
        
        with closing(self.connection.cursor()) as cur:
            
            sqlstring = "select subj_3d_id, lbdat, lbtest, lborres, lbornrhi, lbornrlo, lb_unit from crim_e_lab where subj_3d_id = {} "
            
            cur.execute(sqlstring.format(self.subj_3d_id))
            
            initialTuple = cur.fetchall() # store all the tuple that belongs to this patient in a tuple
            
            
        timematchlist = []
        for item in initialTuple:
            
            if item[1]: # if the date in this tuple is not None
                
                if item[1] != '0000-00-00': # some date are written as 0000-00-00, eliminate these tuples
                    
                    if (item[1] - self.startdate).days >= 0 and  (self.enddate - item[1]).days >= 0:
                        
                        timematchlist.append(item) # select the records that matches the timeline, store in the list 
                        #  in the format of [(subj_3d_id, lbdat, parameter, value, ULN, LLN, unit)]
                    
     
        for item in timematchlist:
            
            item = list(item) # change the type of item from tuple to list
            
            if item[2] in list(self.alias.keys()):
                
                if self.alias[item[2]] in Lrinfo.findPara(self): 
                    
                    item[2] = self.alias[item[2]]  # change the parameter name from name in the lab to name in ae table
                                    
            if item[2] in Lrinfo.findPara(self):  # select the records that matches both the timeline and the parameter
                
                if item[2] in valuedic.keys():
                    
                    valuedic[item[2]].append([item[3]] + [item[4]] + [item[5]] + [item[6]])
                
                else:
                    
                    valuedic[item[2]] = [[item[3]] + [item[4]] + [item[5]] + [item[6]]]
                
                
                # store all the useful information in the dictionary in the format of 
                # {parameter:[[labvalue1, ULN1, LLN1, unit1], [labvalue2, ULN2, LLN2, unit2]...] }
                
        
        return valuedic  # return this dictionary, this dictionary may contains several elements, depending on the number of parameter(s)
                # in current case, there is only one element in each dictionary
                      
        
        
        
        
        
        
        
        
        