# -*- coding: utf-8 -*-
"""
CTCAEinfo - gets the parameter name, primary unit, corresponding rules given a ae name

@author: gengliang.li
"""
import sys

class CTCAEinfo:
    
    # init to define db connection and ae name
    def __init__(self, connection, rules, para, units, aeName): 
        
        self.connection = connection
        self.aeName = aeName
        
        
        self.rules = rules
        self.para = para
        self.units = units
        
        
    # this function is to get the lab parameter givien an ae name 
    def aeParaInfo(self):
        
        para_list = self.para[self.aeName]
        
        return para_list # return the parameter related to this ae in the format of list
        
        
    
    # this function returns the primary unit of parameter
    def aeUnitInfo(self):
        
        para_list = CTCAEinfo.aeParaInfo(self)
        unit_list = self.units[self.aeName]
        
        if len(para_list) != len(unit_list):
            sys.exit()
        
        unit_dic = {}
        
        paraindex = 0
        
        while paraindex < len(para_list):
            
            unit_dic[para_list[paraindex]] = unit_list[paraindex]
            paraindex += 1
            
        return unit_dic # return the unit information in the format of {param1:unit1, param2:unit2...}
        
        
    
    # this function is to get the corresponding rules givien an ae name 
    def aeRuleInfo(self):
        
        rule_list = self.rules[self.aeName]
        
        ruledic = {}
        
        ruledic['rule_grade1' ] = rule_list[0]
        ruledic['rule_grade2' ] = rule_list[1]
        ruledic['rule_grade3' ] = rule_list[2]
        ruledic['rule_grade4' ] = rule_list[3]
        ruledic['rule_grade5' ] = rule_list[4]

        return ruledic # return the rule information in the format of {'rule_grade1':'....', rule_grade2':'...',.... }

    
    
    
    
    
    