import xlwt

#Generate an Excel File to see the Results of kMeans Clustering
class OutputExcel():
    def __init__(self, coordList, ClassList, SubstationNameList):
        self.coordList = coordList
        self.ClassList = ClassList
        self.SubstationNameList = SubstationNameList
        self.wb = xlwt.Workbook()
 

    
    def WriteColumnName(self,ws):
        row_number = 0
        column_number = 0
        for SSname in self.SubstationNameList:
            ws.write(row_number, column_number, SSname + '_VOLT')
            column_number = column_number + 1
            ws.write(row_number, column_number, SSname + '_ANG')
            column_number = column_number + 1
        column_number = column_number + 1
        ws.write(row_number, column_number, 'Class No.')


    def WriteFile(self):
        ws = self.wb.add_sheet('VoltageAngle VS Class')
        self.WriteColumnName(ws)
        row_number = 1
        for coord in self.coordList:
            column_number = 0
            for one_axis in coord:
                ws.write(row_number, column_number, one_axis)
                column_number = column_number + 1
            row_number = row_number + 1

        column_number = column_number + 1
        row_number = 1
        for class_num in self.ClassList:
            ws.write(row_number, column_number, class_num)
            row_number = row_number + 1

        self.wb.save('kMeansResults.xls')
