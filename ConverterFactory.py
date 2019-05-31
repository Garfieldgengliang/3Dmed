# -*- coding: utf-8 -*-
"""
ConverterFactory - avoid repetitive fileName input, make transfer inout easier, package all the codes

@author: gengliang.li
"""
from DbConnection import DbConnection

from Dbinfo import Dbinfo

from AeCompar import AeCompar

from AeConverter import AeConverter


class ConverterFactory:
    
    def __init__(self, fileName):
        
        self.fileName = fileName
        
        Dbconnection = DbConnection(self.fileName)
        self.connection = Dbconnection.connectDb()
        self.db = DbConnection(self.fileName)
               
        Dbinfoset = Dbinfo(self.connection)
        self.rules = Dbinfoset.ctcaeRuleTable() # store the ctcae rule information in this object
        self.para = Dbinfoset.ctcaeParaTable() # store the ctcae parameter information in this object
        self.units = Dbinfoset.ctcaeUnitTable() # store the ctcae units information in this object
        self.alias = Dbinfoset.ctcaeAliaTable() # store the ctcae alias information in this object
        self.unittrans = Dbinfoset.ctcaeUnitTransfer() # store the ctcae mu information in this object
        
    def ConverterLine(self):
        
        AeCompare = AeCompar(self.fileName)
        AeTestlist = AeCompare.aeReal()
        
        TestConvertlist = []
        
        for item in AeTestlist:
            
            print(item)
            
            subj_3d_id = item[0]
#           aespid = item[1]
            aeName = item[2]
            labstartdate = item[6]
            labenddate = item[7]
        
            aeConverter = AeConverter(self.connection, subj_3d_id, labstartdate, labenddate, self.rules, self.para, self.alias, self.units, self.unittrans, aeName )
              #  dbConnection, subj_3d_id, startdate, enddate, rules, para, alias, units, unittrans, aeName)
              
            valuedic = aeConverter.lrInfo()
            
            if valuedic: # if the valuedic is not None
                
                transpre = aeConverter.transPrepare()
                
                if transpre: # if the list that contains rules to be evaluated is not None
                    
                    gradelist = aeConverter.gradeCheker()
                    
                    itemlist = [item[0], item[1], item[2],item[3], item[4], item[5], gradelist]
                    
                    TestConvertlist.append(itemlist)
                    
        if TestConvertlist:
            
            sqlstring =  "delete from cc_ae_grade "
            
            self.db.execute(sqlstring)
            
            
        return TestConvertlist

        # [  [subj_3d_id, aespid, aeName, aestartdate, aeenddate if have one, original_lab_grade , [lab value check grade list]],
        #    [subj_3d_id, aespid, aeName, aestartdate, aeenddate if have one, original_lab_grade , [lab value check grade list]],
        #  ....                                                                                                     ]
        #  lab value check grade list contains all the gardes evaluted from lab values between aestartdate and aeenddate, given the subj_3d_id and aeName from crim_e_ae


ConvertFacTest = ConverterFactory("CCConfig.yaml")

prayforsuccess = ConvertFacTest.ConverterLine()



for elem in prayforsuccess:
    
    print(elem)
    
    if elem[4] == None:
        
        elem[4] = '0000-00-00'

    testdb = DbConnection("CCConfig.yaml")
    
    sqlstring = 'INSERT INTO cc_ae_grade(created_time, created_user, deleted_flag, subj_3d_id, aespid,aeterm, aestdat, aeendat, grade_orig, grade_chk)   \
                             VALUES(NOW() ,"lgl" ,0 , {}, {}, "{}", "{}", "{}", "{}", "{}")'
                             
    testdb.execute(sqlstring.format(elem[0], elem[1], elem[2], elem[3],elem[4], elem[5], elem[6][0]))



