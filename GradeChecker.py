# -*- coding: utf-8 -*-
"""
GradeChecker - return ae grade given rules, parameter and parameter value

@author: gengliang.li
"""

class GradeChecker:
    
    def __init__(self, aeName, rules):
        
        self.aeName = aeName
        self.rules = rules
        
  
    # this function is to return an ae grade given a numeric parameter value
    def checkGrade(self):
        # 还有改进之处 因为有可能 不同的parameter 满足不同的grade 于是返回的grade并不一致
        grade = 0
        if eval(self.rules['rule_grade1']): 
            grade = 'Grade 1'
        elif eval(self.rules['rule_grade2']):
            grade = 'Grade 2'
        elif eval(self.rules['rule_grade3']):
            grade = 'Grade 3'
        elif eval(self.rules['rule_grade4']):
            grade = 'Grade 4'
        elif eval(self.rules['rule_grade5']):
            grade = 'Grade 5'
        else :
            grade = 'Grade -1'

        return grade