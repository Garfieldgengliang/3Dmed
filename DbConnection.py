# -*- coding: utf-8 -*-
"""
DbConnection - define the database which we will use in the software

@author: gengliang.li
"""
import yaml
import os
import pymysql

from contextlib import closing

class DbConnection:
		
	  # init to define the YAML file location
    def __init__(self,  fileName): 
        
        self.fileName = fileName 
        
		
    # get Db info from YAML	
    def getDbInfo(self):	 
        curPath = os.getcwd()
        
        yamlPath = os.path.join(curPath, self.fileName)
        
        f = open(yamlPath, 'r', encoding='utf-8')
        
        cfg = f.read()
        
        d = yaml.load(cfg)
        
        databaseinfor = list(d.values())[0]
        
        return databaseinfor
    
    
	  # use the Db info to connect to the database
    def connectDb(self):  
        
        db = DbConnection.getDbInfo(self)
        
        connection = pymysql.connect(host=db['host'],port=db['port'],                                    
            user=db['user'],passwd=db['password'],db=db['database'],charset=db['charset'])
        
        return connection
    
    def execute(self, sql):
        
        with closing(self.connectDb()) as con:
            
            cursor = con.cursor()
            cursor.execute(sql)
            con.commit()
            




