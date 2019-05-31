# -*- coding: utf-8 -*-
"""
PreProcessor - processing the lab results before grade checker (lln&uln substitute, unit unification )

@author: gengliang.li
"""
import sys    

class PreProcessor:
    
    def __init__(self, connection, valuedic, rules, paraunit, unittrans):
        
        self.valuedic = valuedic # {parameter:[[labvalue1, ULN1, LLN1, unit1], [labvalue2, ULN2, LLN2, unit2]...] }
        self.connection = connection
        self.rules = rules
        self.paraunit = paraunit    
        self.unittrans = unittrans  #  (('g/L', 'Kg/L', '1000', None),('mmol/L', 'mg/dL', '0.05551', 'glucose')...)
        
        
    # this function is to excute unit transformation considering the parameter, 
    # change the numeric value of labresult value, labresult lln, labresult uln
    def unitTransfer(self):
        
        
        labparam = list(self.valuedic.keys())[0] # get the parameter in value dictionary
        
        paramdic = { labparam : [] } # create a new dictionary to store the transfered values, in the format of 
                      # {parameter:[[newlabvalue1, newULN1, newLLN1], [newlabvalue2, newULN2, newLLN2]...] }
        
        primary_unit = self.paraunit[labparam] # find out the primary unit of this parameter
        
        valuelist = self.valuedic[labparam] # [[labvalue1, ULN1, LLN1, unit1], [labvalue2, ULN2, LLN2, unit2]...]
                      
        for item in valuelist:  
            
            if item[0]: # if the labvalue in this item is not None
            
                lab_unit = item[3]  # find out the lab unit of this parameter
                
                if primary_unit == lab_unit:
                    
                    value_uln_lln_list = [item[0], item[1], item[2]]
                    # store labvalue, lln and uln in a dictionary in the format of {parameter:[value,lln,uln]}
                
                else:
                    
                    useful_param_list = []
                    
                    useful_unittrans_list = []
                    
                    for elem in self.unittrans: # check the cc_dict_mu unit transfer table
                        
                        if elem[0] == primary_unit and elem[1] == lab_unit:
                            
                            useful_unittrans_list.append(elem)
                            
                            useful_param_list.append(elem[3])
                    
                            
                    
                    if labparam in useful_param_list:  # if the unit transformation is parameter specialitic
                        
                        paralistindex = useful_param_list.index(labparam)  
                        measurement = float(useful_unittrans_list[paralistindex][2]) # get the measurement between two differnet units 
                        
                        transvalue = (float(item[0])) * measurement
                        ulnvalue =  (float(item[1])) * measurement
                        llnvalue =  (float(item[2])) * measurement
                        
                        value_uln_lln_list = [transvalue, ulnvalue, llnvalue]
                       
                    else:   #if the unit transformation is not related to parameter
                        
                        if useful_unittrans_list == []: # if there is no element in useful_unittrans_list, then there should be some problem with unit
                        # the possible problems can be: 1. the unit in lab value cannot be retrieved in unit transfer table
                        #                               2. the primary unit in cc_dict_ae does not correspond to the primary unit in unit transfer table(cc_dict_mu)
                        #                               3.  .......
                            sys.exit()
    
                        measurement = float(useful_unittrans_list[0][2])
                        
                        transvalue = (float(item[0])) * measurement
                        ulnvalue =  (float(item[1])) * measurement
                        llnvalue = (float(item[2])) * measurement
                        
                        value_uln_lln_list = [transvalue, ulnvalue, llnvalue]
                       
                paramdic[labparam].append(value_uln_lln_list)
            
        return paramdic # return the dictionary after unit transform in the format of
                        #  {parameter:[[newlabvalue1, newULN1, newLLN1], [newlabvalue2, newULN2, newLLN2]...] }
    
    
    
    # this function is to replace all the parameters, ulns and llns in rules    
    def rulesPrepare(self):
              
             
        paramdic = PreProcessor.unitTransfer(self)
        
        new_rule_list = [] # create a new list to store different sets of rules, each set contains five samll rules ( in the form of dictionary )
        
        param = list(paramdic.keys())[0]
        
        for elem in paramdic[param]:
            
            new_rule_dic = {}
            
            for item in self.rules.items() : # process one rule in the rule dictionary once at a time
                
                rulegrade, rulevalue = item  
                
                if rulevalue != None: 
                    
                    currentrulelist = rulevalue.split(' or ')  # split every rule into small pieces, the first small piece is all about first parameter, and 
                                                            # the second small piece is all about second parameter and so on...and store all the splited rules in a list
                    ruleindex = 0  # give the splited rules an index
                    
                    while ruleindex < len(currentrulelist):
                        
                        if param in currentrulelist[ruleindex]:  # if the param in lab param dictionary corresponds to this splited small rule      
                            
                            currentrulelist[ruleindex] = currentrulelist[ruleindex].replace(param, str(elem[0]))
                            #substitute parameter with its value
                            currentrulelist[ruleindex] = currentrulelist[ruleindex].replace('ULN', str(elem[1]))
                            # substitute parameter lln with its lln
                            currentrulelist[ruleindex] = currentrulelist[ruleindex].replace('LLN', str(elem[2]))
                            # substitute parameter uln with its uln
                            
                                
                        else:
                            currentrulelist[ruleindex] = " 1<0 " # if the param does not correspond to this small splited rule, then substitute this rule with sth False
                            
                        ruleindex += 1
                    
                    current_rule_merge = " or ".join(currentrulelist) # merge the rule
                    new_rule_dic[rulegrade] = current_rule_merge  # store the rule in a dictionary
                
                else:
                    new_rule_dic[rulegrade] = " 1<0 " # if the rule is None, substitute it with sth False
                    
            new_rule_list.append(new_rule_dic)
                
        return new_rule_list # the format of this list is like [ { rule_grade1:'a string', rule_grade2:'a string',...rule_grade5:'a string'} , 
                             #                                    { rule_grade1:'a string', rule_grade2:'a string',...rule_grade5:'a string'} , 
                             #                                    ... , { rule_grade1:'a string', rule_grade2:'a string',...rule_grade5:'a string'}]            
                          

        
        
        
        
        
        
        
        
        
        
        
        
        