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

    #Get a list of voltage and angle of this substation, from time 1 to time 20
    def VoltageAngleList(self, time_list):
        self.VoltageList = list()
        self.AngleList = list()
        for time in time_list:
            (angle, voltage) = self.ReadVoltageAngle(time)
            self.VoltageList.append(voltage)
            self.AngleList.append(angle)
        self.conn.commit()


