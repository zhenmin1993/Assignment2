import pymysql.cursors
from Substation import *

class DataRead():
    def __init__(self,cur,conn):
        self.cur = cur
        self.conn = conn

    def ReadSubstationNameID(self):
        self.SubstationNameID_Dict = dict()
        self.SubstationName_List = list()
        self.SubstationID_List = list()
        sql_SSNameID = '''SELECT rdfid, name FROM substations'''
        self.cur.execute(sql_SSNameID)
        SubstationNameIDs = self.cur.fetchall()
        for SubstationNameID in SubstationNameIDs:
            self.SubstationNameID_Dict[SubstationNameID['name']] = SubstationNameID['rdfid']
            self.SubstationName_List.append(SubstationNameID['name'])
            self.SubstationID_List.append(SubstationNameID['rdfid'])

        #return SubstationNameIDs
        #print(self.SubstationNameID_Dict)

    def getTimeList(self, tableName):
        TimeList = list()
        sql_getTimeList = 'SELECT time FROM ' + tableName
        self.cur.execute(sql_getTimeList)
        AllTimes = self.cur.fetchall()
        for one_time in AllTimes:
            if one_time['time'] in TimeList: continue
            TimeList.append(one_time['time'])
        TimeList.sort()
        return TimeList

    def FetchData(self, tableName):
        TimeList = self.getTimeList(tableName)
        self.ReadSubstationNameID()
        self.SubstationInstanceList = list()
        for SubstationID in self.SubstationID_List:
            one_instance = Substation(SubstationID,self.cur, self.conn)
            one_instance.VoltageAngleList(TimeList)
            self.SubstationInstanceList.append(one_instance)
        #print(self.SubstationInstanceList)

    

