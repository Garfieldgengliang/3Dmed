# -*- coding: utf-8 -*-
"""
AeConverter - convert lab result into ae grade given lab result information and ae name

@author: gengliang.li
"""


from CTCAEinfo import CTCAEinfo

from Lrinfo import Lrinfo

from PreProcessor import PreProcessor

from GradeChecker import GradeChecker


class AeConverter:
    
    def __init__(self, dbConnection, subj_3d_id, startdate, enddate, rules, para, alias, units, unittrans, aeName):
          
        self.dbConnection = dbConnection
        
        self.subj_3d_id = subj_3d_id
        self.startdate = startdate
        self.enddate = enddate
        
        self.rules = rules
        self.para = para
        self.units = units
        self.alias = alias
        self.unittrans = unittrans
        
        self.aeName = aeName
        
        
    # gets the primary unit and corresponding rules given a ae name        
    def ctcaeInfo(self):
        
        ctcaeinfoCatch = CTCAEinfo(self.dbConnection, self.rules, self.para, self.units, self.aeName)  
        
        unit = ctcaeinfoCatch.aeUnitInfo() # get the parameter units dictionary
        
        rules = ctcaeinfoCatch.aeRuleInfo() # get the rule dictionary
        
        aeInfodic = {'unit':unit, 'rules':rules}
        return aeInfodic # store all the ctcae information about units and rules in this dictionary, makes it a 
                         # dictionary of dictionary

    # get the lab information and store them in a dictionary   
    def lrInfo(self):
                      
        labResultCatch = Lrinfo(self.dbConnection, self.subj_3d_id, self.startdate, self.enddate, self.rules, self.para, self.alias, self.units, self.aeName)
    
        labInfodic = labResultCatch.valueLlnUlnUnitInfo()
        
        return labInfodic # store all the useful information in the dictionary in the format of 
                          # {parameter:[[labvalue1, ULN1, LLN1, unit1], [labvalue2, ULN2, LLN2, unit2]...] }
                          # in current case, there is only one element in each dictionary
        
        
    # processing the lab results before grade checker (lln&uln substitute, unit unification )
    def transPrepare(self):
        
        ctcaeinfo = AeConverter.ctcaeInfo(self)       
        valuedic = AeConverter.lrInfo(self)
        
        rules = ctcaeinfo['rules']
        paraunit = ctcaeinfo['unit']
        
        preparation = PreProcessor(self.dbConnection, valuedic, rules, paraunit, self.unittrans )
        
        rulesTransfered = preparation.rulesPrepare()
        
        return  rulesTransfered  # the format of this list is like [ { rule_grade1:'a string', rule_grade2:'a string',...rule_grade5:'a string'} , 
                                 #                                  { rule_grade1:'a string', rule_grade2:'a string',...rule_grade5:'a string'} , 
                                 #                             ... , { rule_grade1:'a string', rule_grade2:'a string',...rule_grade5:'a string'}]            
                          
       
    # return ae grade given rules, parameter and parameter value
    def gradeCheker(self):
        
        ruleslist =  AeConverter.transPrepare(self)
        
        gradelist = []
        
        for elem in ruleslist:
            
            gradetrans = GradeChecker(self.aeName, elem)
            
            grade = gradetrans.checkGrade()
            
            gradelist.append(grade)
        

        return gradelist
        
        
        
        
        
        