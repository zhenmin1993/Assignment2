import math
import copy
import pymysql.cursors

class Substation():
    def __init__(self, rdfID, cur,conn):
        self.rdfID = rdfID
        self.cur = cur
        self.conn = conn

    #Get the substation name
    def ReadName(self):
        sql_readName = '''SELECT name FROM substations where rdfid = %s'''
        self.cur.execute(sql_readName, (self.rdfID,))
        self.name = self.cur.fetchone()['name']
        #print(self.name)

    #Get the voltage and angle at one certain mesurement time
    def ReadVoltageAngle(self,time):
        self.ReadName()
        sql_readVoltageAngle = '''SELECT name, value FROM measurements where (sub_rdfid , time) = (%s, %s)'''
        self.cur.execute(sql_readVoltageAngle, (self.rdfID,time))
        VoltageAngles = self.cur.fetchall()
        #print(VoltageAngles)
        for VoltAng in VoltageAngles:
            if '_ANG' in VoltAng['name']:
                one_angle = VoltAng['value']
        for VoltAng in VoltageAngles:
            if '_VOLT' in VoltAng['name']:
                one_voltage = VoltAng['value']
            #print((one_angle, one_voltage))
        return (one_angle, one_voltage)

    #Get a list of voltage and angle of this substation, from time 1 to time 200
    def VoltageAngleList(self, time_list):
        self.VoltageList = list()
        self.AngleList = list()
        self.puAngleList = list()
        for time in time_list:
            (angle, voltage) = self.ReadVoltageAngle(time)
            self.VoltageList.append(voltage)
            self.AngleList.append(angle)
        self.conn.commit()
        #print(self.VoltageList)
        #print(self.AngleList)
        self.NormalVoltageList = self.FeatureScaling(self.VoltageList)
        self.NormalAngleList = self.FeatureScaling(self.AngleList)
        #print(self.NormalAngleList)

    def FeatureScaling(self,one_list):
        ValueSum = 0
        ValueNum = 0
        for item in one_list:
            ValueSum = ValueSum + item
            ValueNum = ValueNum + 1

        ValueAverage = ValueSum/ValueNum

        normalisedList = list()

        if max(one_list) != min(one_list):
            for item in one_list:
                one_value = (item - ValueAverage)/(max(one_list)-min(one_list))
                normalisedList.append(one_value)

        if max(one_list) == min(one_list):
            for item in one_list:
                normalisedList.append(item)
            #print(one_value)
        return normalisedList





