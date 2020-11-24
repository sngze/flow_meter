import pymysql
import time
from datetime import datetime

class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  user='raspi',
                                  password='0000',
                                  db='brewants',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)
 
    def executeAll(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        return row
    
    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def commit(self):
        self.db.commit()

    def select(self):
         date = "{}-{}-{}".format(datetime.today().year, datetime.today().month, datetime.today().day)
         sql = "select menu, liters from flow_meter where date = %s order by line;"
         row = self.executeAll(sql,date)
         return row


    def distinctselect(self,table):
         sql = " SELECT DISTINCT s_id FROM silver_db."+table+";"    
         row = self.executeAll(sql)
         return row

    def select_s_id(self,table,s_id):
         sql = "SELECT * FROM silver_db."+table+" where s_id="+s_id+";"
         row = self.executeAll(sql)
         return row
