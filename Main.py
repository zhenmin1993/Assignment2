from DataRead import *

from tkinter import *
import tkinter as tk
import pymysql.cursors

from kMeans import *
from kNN import *
from PlotDiameter import *
from OptimizeK import *
from OutputExcel import *

from GUI import *



import sys
import os
import time


import math
import copy






#define the function of LogIn Button
#This button is used to connect the MySQL Server
def LoginButtonFunc(): 
    #print 'Connecting to MySQL server'
    Message = 'Connecting to MySQL server'

    var_Log.set(Message)
    Stat_Para_Log_Init = {'bd':1,'anchor':W, 'fg':'black'}
    win.AddStatus(Stat_Para_Log_Init, LogStructStatus, var_Log.get())
    win.root.update()

    host =  var_host.get()
    user = var_user.get()
    passwd =  var_passwd.get()
    db =  var_dbName.get()
    port =  var_port.get()
    port = int(port)

    config = {
          'host':host,
          'port':port,
          'user':user,
          'password':passwd,
          'db':db,
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
 
    # Connect to the database


    try:
        global connection
        #global cursor
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            Message = 'Connected to MySQL server'
            #print 'Connected to MySQL server\n'

            var_Log.set(Message)
            Stat_Para_Log_success = {'bd':1,'anchor':W, 'fg':'#228B22'}
            win.AddStatus(Stat_Para_Log_success, LogStructStatus, var_Log.get())
            win.root.update()
            messagebox.showinfo(title='Computer Application', \
                message='Server Connected! Please Continue!')


    except:
        Message = 'Connection Failed! Please Check!'
        #print 'Connection Failed! Please Check!'

        var_Log.set(Message)
        Stat_Para_Log_fail = {'bd':1,'anchor':W, 'fg':'red'}
        win.AddStatus(Stat_Para_Log_fail, LogStructStatus, var_Log.get())
        win.root.update()

#This function provide the user one possible reference to choose suitable k number
#This function is optional
def OptimizeKFunc():
    with connection.cursor() as cursor:
        dr = DataRead(cursor, connection)
        TimeList = dr.getTimeList('measurements')
        #print(TimeList)
        dr.FetchData('measurements')
        #print(dr.SubstationInstanceList[0].VoltageList)
        TrainingExample_num = len(TimeList)

        k_list = [1,2,3,4,5,6]
        nn = OptimizeK(k_list, dr.SubstationInstanceList, TrainingExample_num)
        Diameter_dict = nn.k_diameter()

        pp = PlotDiameter(k_list,Diameter_dict)
        pp.Plot()

#Run kMeans Clustering Function
def Run_kMeans():
    try:
        with connection.cursor() as cursor:

            if var_ClusterNumber.get() == None:
                messagebox.showinfo(title='Computer Application', \
                message='Cluster Number May Not be Empty')

            if var_ClusterNumber.get() != None:

                try:
                    cluster_num = int(var_ClusterNumber.get())
                except:
                    cluster_num = -1
                    messagebox.showinfo(title='Computer Application', \
                    message='Please Input Vaid Cluster Number!')

                if cluster_num >= 0:
                    TrainingData = DataRead(cursor, connection)
                    TimeList = TrainingData.getTimeList('measurements')
                    #print(TimeList)
                    TrainingData.FetchData('measurements')
                    #print(TrainingData.SubstationInstanceList[0].VoltageList)
                    TrainingExample_num = len(TimeList)
                    global assign_point_list
                    #cluster_num = int(var_ClusterNumber.get())
                    assign_point_list = kMeans(cluster_num, TrainingData.SubstationInstanceList, TrainingExample_num).kMean_Algorithm()
                    coordList = list()
                    original_coordList = list() 
                    ClassList = list()
                    SubstationNameList = TrainingData.SubstationName_List
                    for example in assign_point_list:
                        coordList.append(example.coordinate)
                        original_coordList.append(example.original_coordinate)
                        ClassList.append(example.inClass)
                    #print(coordList)

                    ExcelFile = OutputExcel(coordList, original_coordList, ClassList, SubstationNameList)
                    ExcelFile.WriteFile()

                    Message = 'kMeans Clustering Succeed!'
                    var_kMeansCheck.set(Message)

                    Stat_Para_kMeansCheck = {'bd':1,'anchor':W, 'fg':'#228B22'}
                    kMeansCheckStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
                    win.AddStatus(Stat_Para_kMeansCheck, kMeansCheckStructStatus, var_kMeansCheck.get())
                    win.root.update()

                    messagebox.showinfo(title='Computer Application', \
                    message='kMeans Clustering Finished! Now you can run kNN! \n Results are Stored in File "kMeansResults.xls"!')

    except:
            Message = 'kMeans Clustering Failed! Please Check'
            var_kMeansCheck.set(Message)

            Stat_Para_kMeansCheck = {'bd':1,'anchor':W, 'fg':'red'}
            kMeansCheckStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
            win.AddStatus(Stat_Para_kMeansCheck, kMeansCheckStructStatus, var_kMeansCheck.get())
            win.root.update()

#After Running kMeans clustering, run kNN
def Run_kNN():
    try:
        with connection.cursor() as cursor:
            ValidateSet = DataRead(cursor, connection)
            TimeList_valid = ValidateSet.getTimeList('analog_values')
            ValidateSet.FetchData('analog_values')

            cluster_num = int(var_ClusterNumber.get())

            global ClassificationDict
            ClassificationDict = dict()
            for item in range(cluster_num):
                ClassificationDict[item] = list()

            for iter_valid in range(len(TimeList_valid)):
                coord_valid = list()
                for SubstationInstance in  ValidateSet.SubstationInstanceList:
                    coord_valid.append(SubstationInstance.NormalVoltageList[iter_valid])
                    coord_valid.append(SubstationInstance.NormalAngleList[iter_valid])


                one_Validation = kNN(assign_point_list,coord_valid)
                NearestNeighNumber = int(var_NearNeighNumber.get())
                one_Classification = one_Validation.AssignClass(NearestNeighNumber)
                ClassificationDict[one_Classification].append(TimeList_valid[iter_valid])



            Message = 'kNN Classification Succeed!'
            var_kNNCheck.set(Message)

            Stat_Para_kNNCheck = {'bd':1,'anchor':W, 'fg':'#228B22'}
            kNNCheckStructStatus = {'row':17, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
            win.AddStatus(Stat_Para_kNNCheck, kNNCheckStructStatus, var_kNNCheck.get())
            win.root.update()

            Label_Message = None
            Lab_Para_Bus = {'bg':None, 'fg':'white'}
            BusStructLab = {'row':1,'columnspan':10, 'sticky':N+E+S+W, 'rowspan':15, 'column':6}
            win.AddLabel(Label_Message , Lab_Para_Bus, BusStructLab)

            Lab_Para_Bus_Title = {'bg':'grey60', 'fg':'black'}
            BusStructLabTitle = {'row':0,'columnspan':10, 'sticky':N+E+S+W, 'rowspan':1, 'column':6}
            win.AddLabel('Please Input the Class Name Below' , Lab_Para_Bus_Title, BusStructLabTitle)

            global class_name_list
            class_name_list = list()
            column_number = 6
            for item in range(cluster_num):
                var_class_name=StringVar()
                var_class_name.set(item)
                class_name_list.append(var_class_name)


                Entr_class_name = {'off':400,'on':300, 'show':None}
                class_name_StructEntr = {'row':2, 'column':column_number,'sticky':N+E+S+W}
                win.AddEntry(var_class_name, Entr_class_name , class_name_StructEntr)

                Lab_Para_class_name = {'bg':None, 'fg':'black'}
                class_nameStructLab = {'row':1,'columnspan':1, 'sticky':N+E+S+W, 'rowspan':1, 'column':column_number}
                win.AddLabel('Name of Class'+str(item)+':' , Lab_Para_class_name, class_nameStructLab )

                column_number = column_number + 1

            ClassNameButt = {'row':3,'column':column_number -1 ,'padx':4,'pady':1, 'columnspan':1}
            win.AddButton('Confirm', output_kNN, ClassNameButt)
            win.root.update()
    
    except:

            Message = 'kNN Classification Failed!'
            var_kNNCheck.set(Message)

            Stat_Para_kNNCheck = {'bd':1,'anchor':W, 'fg':'red'}
            kNNCheckStructStatus = {'row':17, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
            win.AddStatus(Stat_Para_kNNCheck, kNNCheckStructStatus, var_kNNCheck.get())
            win.root.update()



#Define the ExitButtonFunction
def ExitButtonFunc():
    answer = messagebox.askquestion('Computer Application', 'Are you sure to EXIT?')

    if answer == 'yes':
        win.DestroySelf()      
        sys.exit()



#The function to output kNN results
def output_kNN():
    ClassName = dict()
    for iter_name in range(len(ClassificationDict)):
        ClassName[iter_name] = class_name_list[iter_name].get()

    row_number = 4
    for key_kNN, value_kNN in ClassificationDict.items():
        column_number = 6
        new_column_number = 0
        Lab_Para_Class_Name = {'bg':'grey', 'fg':'black'}
        Class_NameStructLab = {'row':row_number,'columnspan':7, 'sticky':N+E+S+W, 'rowspan':1, 'column':column_number}
        win.AddLabel(ClassName[key_kNN], Lab_Para_Class_Name, Class_NameStructLab)
        for value in value_kNN:
            if new_column_number == 5:
                row_number = row_number + 1
                new_column_number = 0
                column_number = 6
            Stat_Para_Time = {'bd':1,'anchor':W, 'fg':'black'}
            TimeStructStat = {'row':row_number + 1,'columnspan':1, 'sticky':N+E+S+W, 'column':column_number}
            win.AddStatus( Stat_Para_Time, TimeStructStat, 'Time '+str(value))
            new_column_number = new_column_number + 1
            column_number = column_number + 1

        row_number = row_number + 2

    Lab_Para_Bus_Title = {'bg':'grey60', 'fg':'black'}
    BusStructLabTitle = {'row':0,'columnspan':10, 'sticky':N+E+S+W, 'rowspan':1, 'column':6}
    win.AddLabel('kNN Classification on Validation Set' , Lab_Para_Bus_Title, BusStructLabTitle)
    win.root.update()





#Initialize the GUI window frame
win = MyWindow()


Lab_Para_Title = {'bg':'grey', 'fg':'black'}
TitleStructLab = {'row':0,'columnspan':4, 'sticky':N+E+S+W , 'rowspan':1, 'column':0}
win.AddLabel('Computer Application in Power Systems\n Assignment 2' , Lab_Para_Title, TitleStructLab  )


Lab_Para_Log = {'bg':'brown', 'fg':'white'}
LogStructLab = {'row':1,'columnspan':4, 'sticky':N+E+S+W , 'rowspan':1, 'column':0}
win.AddLabel('Please Log In First' , Lab_Para_Log, LogStructLab )


Lab_Para_host = {'bg':None, 'fg':'black'}
hostStructLab = {'row':2,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('host' , Lab_Para_host, hostStructLab)


global var_host
var_host=StringVar()
var_host.set('127.0.0.1')

Entr_Para_host = {'off':400,'on':300, 'show':None}
hostStructEntr = {'row':2, 'column':1,'sticky':W}
win.AddEntry(var_host , Entr_Para_host , hostStructEntr)


Lab_Para_User = {'bg':None, 'fg':'black'}
UserStructLab = {'row':3,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('User' , Lab_Para_User, UserStructLab)


global var_user
var_user=StringVar()
var_user.set('root')

Entr_Para_User = {'off':400,'on':300, 'show':None}
UserStructEntr = {'row':3, 'column':1,'sticky':W}
win.AddEntry(var_user, Entr_Para_User , UserStructEntr)



Lab_Para_Passwd = {'bg':None, 'fg':'black'}
PasswdStructLab = {'row':4,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Password' , Lab_Para_Passwd, PasswdStructLab)


global var_passwd
var_passwd=StringVar()
var_passwd.set('1993')

Entr_Para_Passwd = {'off':400,'on':300, 'show':'*'}
PasswdStructEntr = {'row':4, 'column':1,'sticky':W}
win.AddEntry(var_passwd, Entr_Para_Passwd , PasswdStructEntr)



Lab_Para_dbName = {'bg':None, 'fg':'black'}
dbNameStructLab = {'row':5,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Database Name' , Lab_Para_dbName, dbNameStructLab)


global var_dbName
var_dbName=StringVar()
var_dbName.set('9bus')

Entr_Para_dbName = {'off':400,'on':300, 'show':None}
dbNameStructEntr = {'row':5, 'column':1,'sticky':W}
win.AddEntry(var_dbName, Entr_Para_dbName , dbNameStructEntr)



Lab_Para_Port = {'bg':None, 'fg':'black'}
PortStructLab = {'row':6,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Port' , Lab_Para_Port, PortStructLab)


global var_port
var_port=StringVar()
var_port.set(3306)

Entr_Para_Port = {'off':400,'on':300, 'show':None}
PortStructEntr = {'row':6, 'column':1,'sticky':W}
win.AddEntry(var_port, Entr_Para_Port , PortStructEntr)



LogStructImag = {'row':2,'rowspan':4,'columnspan':2, 'column':2,'sticky':W+E+N+S, 'padx':5, 'pady':5}
file_name = 'pic2.gif'
win.AddImage('pic2.gif', LogStructImag)


LogStructButt = {'row':7,'column':2,'padx':4,'pady':1, 'columnspan':1}
win.AddButton('Log In', LoginButtonFunc, LogStructButt)


ExitStructButt = {'row':7,'column':3,'padx':4,'pady':1, 'columnspan':1}
win.AddButton('Exit', ExitButtonFunc, ExitStructButt)



global var_Log
var_Log=StringVar()
var_Log.set('Waiting For Operation')


Stat_Para_Log = {'bd':1,'anchor':W, 'fg':'black'}
LogStructStatus = {'row':8, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}

win.AddStatus(Stat_Para_Log, LogStructStatus, var_Log.get())



Lab_Para_FileName = {'bg':'brown', 'fg':'white'}
FileNameStructLab = {'row':9,'columnspan':4, 'sticky':N+E+S+W, 'rowspan':1, 'column':0}
win.AddLabel('Input or Use Optimize to Help Choosing the Cluster Number' , Lab_Para_FileName, FileNameStructLab)


global var_TrainDataTableName
var_TrainDataTableName=StringVar()
var_TrainDataTableName.set('measurements')

Entr_TrainDataTableName = {'off':400,'on':300, 'show':None}
TrainDataTableNameStructEntr = {'row':10, 'column':1,'sticky':W}
win.AddEntry(var_TrainDataTableName, Entr_TrainDataTableName , TrainDataTableNameStructEntr)

Lab_Para_TrainDataTableName = {'bg':None, 'fg':'black'}
TrainDataTableNameStructLab = {'row':10,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Training Data Set Table Name:' , Lab_Para_TrainDataTableName, TrainDataTableNameStructLab )

global var_ClusterNumber
var_ClusterNumber=StringVar()

Entr_ClusterNumber = {'off':400,'on':300, 'show':None}
ClusterNumberStructEntr = {'row':11, 'column':1,'sticky':W}
win.AddEntry(var_ClusterNumber, Entr_ClusterNumber , ClusterNumberStructEntr)


Lab_Para_ClusterNumber = {'bg':None, 'fg':'black'}
ClusterNumberStructLab = {'row':11,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Cluster Number:' , Lab_Para_ClusterNumber, ClusterNumberStructLab )

OptimizeKButt = {'row':12,'column':0,'padx':4,'pady':1, 'columnspan':2}
win.AddButton('Optional : Plot Diameter to Optimize Cluster Number', OptimizeKFunc, OptimizeKButt)

kMeansButt = {'row':12,'column':2,'padx':4,'pady':1, 'columnspan':1}
win.AddButton('Run kMeans', Run_kMeans, kMeansButt)

global var_ValidDataTableName
var_ValidDataTableName=StringVar()
var_ValidDataTableName.set('analog_values')

Entr_ValidDataTableName = {'off':400,'on':300, 'show':None}
ValidDataTableNameStructEntr = {'row':13, 'column':1,'sticky':W}
win.AddEntry(var_ValidDataTableName, Entr_ValidDataTableName , ValidDataTableNameStructEntr)



Lab_Para_ValidDataTableName = {'bg':None, 'fg':'black'}
ValidDataTableNameStructLab = {'row':13,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Validation Data Set Table Name:' , Lab_Para_ValidDataTableName, ValidDataTableNameStructLab )

global var_NearNeighNumber
var_NearNeighNumber=StringVar()
var_NearNeighNumber.set(3)

Entr_NearNeighNumber = {'off':400,'on':300, 'show':None}
NearNeighNumberStructEntr = {'row':14, 'column':1,'sticky':W}
win.AddEntry(var_NearNeighNumber, Entr_NearNeighNumber , NearNeighNumberStructEntr)

Lab_Para_NearNeighNumber = {'bg':None, 'fg':'black'}
NearNeighNumberStructLab = {'row':14,'columnspan':1, 'sticky':E, 'rowspan':1, 'column':0}
win.AddLabel('Nearest Neighbor Number:' , Lab_Para_NearNeighNumber, NearNeighNumberStructLab )

kNNButt = {'row':15,'column':2,'padx':4,'pady':1, 'columnspan':1}
win.AddButton('Run kNN', Run_kNN, kNNButt)


Exit2StructButt = {'row':15,'column':3,'padx':4,'pady':1, 'columnspan':1}
win.AddButton('Exit', ExitButtonFunc, Exit2StructButt)


global var_kMeansCheck
var_kMeansCheck=StringVar()

Stat_Para_kMeansCheck = {'bd':1,'anchor':W, 'fg':'black'}
kMeansCheckStructStatus = {'row':16, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_kMeansCheck, kMeansCheckStructStatus, var_kMeansCheck.get())


global var_kNNCheck
var_kNNCheck=StringVar()

Stat_Para_kNNCheck = {'bd':1,'anchor':W, 'fg':'black'}
kNNCheckStructStatus = {'row':17, 'sticky':N+E+S+W, 'columnspan':3, 'column':0}
win.AddStatus(Stat_Para_kNNCheck, kNNCheckStructStatus, var_kNNCheck.get())

ClassNameButt = {'row':3,'column':10,'padx':4,'pady':1, 'columnspan':1}
win.AddButton('Confirm', output_kNN, ClassNameButt)





Lab_Para_Separate = {'bg':None, 'fg':None}
SeparateStructLab = {'row':0,'columnspan':1, 'sticky':E, 'rowspan':17, 'column':4}
win.AddLabel(None, Lab_Para_Separate, SeparateStructLab)


Lab_Para_Bus_Title = {'bg':'grey60', 'fg':'black'}
BusStructLabTitle = {'row':0,'columnspan':10, 'sticky':N+E+S+W, 'rowspan':1, 'column':6}
win.AddLabel('kNN Classification on Validation Set' , Lab_Para_Bus_Title, BusStructLabTitle)


Label_Message = 'kNN Classification Results Will Be Shown Here'
Lab_Para_Bus = {'bg':'brown', 'fg':'white'}
BusStructLab = {'row':1,'columnspan':10, 'sticky':N+E+S+W, 'rowspan':15, 'column':6}
win.AddLabel(Label_Message , Lab_Para_Bus, BusStructLab)


win.root.mainloop()