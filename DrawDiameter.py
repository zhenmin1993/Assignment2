#import string
import matplotlib.pyplot as plt  
import numpy as np
#import math
#import copy
from kMeans import *
from OptimizeK import *
 
class PlotDiameter():
    def __init__(self, k_list, Diameter_dict):
        self.k_list = k_list
        self.Diameter_list = list()
        for key_dia, value_dia in Diameter_dict.items():
            for kValue in k_list:
                if kValue == key_dia:
                    self.Diameter_list.append(value_dia)



    def Plot(self):
        plt.plot(self.k_list,self.Diameter_list)
        plt.xlabel('Value of k')
        plt.ylabel('Cluster Diameter')
        plt.show()

