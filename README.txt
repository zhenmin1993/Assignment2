***** This project is finished by Zhenmin Tao (Zhenmin@kth.se) and Mian Xiong(mxiong@kth.se) *****

***** Before running the program, you need to create a database called '9Bus' in your MySQL Server *****

***** The environment is Python 3.5.2 *****

***** Existing Module Used : *****
***** pymysql : operate DB *****
***** matplotlib : Draw Graph *****
***** xlwt : generate excel(xls) file *****
***** Modules are installed with "easy_install pip" tools *****



***** Brief introduction of each file: *****
1.kMeans.py
  The algorithm of kMeans Clustering.

2.kNN.py
  The algorithm of k Nearest Neighbor, taking kMeans output as input

3.DataRead.py
  Read all the data from database

4.OptimizeK.py & PlotDiameter.py
  This is an optional function to enable flexible input of arbitrary data, user can choose value of k with the aid of the cluster diameter graph.

5.Substation.py
  A class of Substation with method to read information related to each substation

6.TrainingExample.py
  Build training example based on the data read from database

7.OutputExcel.py
  Generate a excel file to store the result of kMeans in order to do further analysis

7.GUI.py
  A class for GUI window frame.


*****Please contact us if you met any problem******