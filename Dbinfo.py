# -*- coding: utf-8 -*-
"""
Dbinfo -- store information of CTCAE and unit transfer table in several objects 
and in this way, we can avoid connecting database to fetch these information every time we test a lab result

@author: gengliang.li
"""

from contextlib import closing

class Dbinfo:
    
    def __init__(self,  connection): 
        self.connection = connection
        
    # get the whole rules table and store it in an object    
    def ctcaeRuleTable(self):
        
        with closing(self.connection.cursor()) as cur:
            
            sqlstring =  "select name, rule_grade1, rule_grade2, rule_grade3, rule_grade4, rule_grade5 from cc_dict_ae "
          
            cur.execute(sqlstring)
            
            targetform = cur.fetchall()
            
        targetdic = {}
        
        for elem in targetform:
        
            valuelist = [elem[1]] + [elem[2]] + [elem[3]] + [elem[4]] + [elem[5]]
        
            targetdic[elem[0]] = valuelist

        return targetdic # store information about rules in the format of {aeName:[rule_grade1, rule_grade2, rule_grade3, rule_grade4, rule_grade5]}


    # get the whole parameter table and store it in an object
    def ctcaeParaTable(self):
        
        with closing(self.connection.cursor()) as cur:
            
            sqlstring =  "select name, param from cc_dict_ae "
          
            cur.execute(sqlstring)
            
            targetform = cur.fetchall()
            
        targetdic = {}
    
        for elem in targetform:
    
            para_list =  elem[1].split(',') 
        
            targetdic[elem[0]] = para_list
            
        return targetdic  # store information about rules in the format of {aeName:[param1, param2...]}
    
    # get the whole unit table and store it in an object
    def ctcaeUnitTable(self):
        
        with closing(self.connection.cursor()) as cur:
            
            sqlstring =  "select name, unit from cc_dict_ae "
          
            cur.execute(sqlstring)
            
            targetform = cur.fetchall()
            
        targetdic = {}
    
        for elem in targetform:
    
            unit_list =  elem[1].split(',') 
        
            targetdic[elem[0]] = unit_list
            
        return targetdic   # store information about rules in the format of {aeName:[unit1, unit2...]}
        
    # get all the parameter alias information from alias table
    def ctcaeAliaTable(self):
        
        with closing(self.connection.cursor()) as cur:
        
            sqlstring =  "select name, alias from cc_dict_alias "
            
            cur.execute(sqlstring)
            
            targetform = cur.fetchall()
            
        targetdic = {}
    
        for elem in targetform:
    
            currentalia =  elem[1] 
        
            targetdic[currentalia] = elem[0]
            
        return targetdic  # store the alias information in the format of {alia:standard name}
            
    def ctcaeUnitTransfer(self):
        
        with closing(self.connection.cursor()) as cur:
            
            sqlstring = "select primary_mu, derived_mu, rel, param from cc_dict_mu " 
            
            cur.execute(sqlstring)
           
            targetTrans = cur.fetchall()  # get the primary unit, derived unit, param and transrules 
        
        return targetTrans #  (('g/L', 'Kg/L', '1000', None),('mmol/L', 'mg/dL', '0.05551', 'glucose')...)
    
    

        