from DataRead import *
from TrainingExample import *
import math
import copy
from kMeans import *

class OptimizeK():
    def __init__(self, k_list, data_list, TrainingExample_num):
        self.k_list = k_list
        self.data_list = data_list
        self.TE_num = TrainingExample_num


        #self.assign_point_list = kMeans(cluster_num, data_list).kMean_Algorithm()

    def kMeans_with_different_k(self):
        self.assign_point_list_dict = dict()
        for kValue in self.k_list:
            assign_point_list = kMeans(kValue, self.data_list, self.TE_num).kMean_Algorithm()
            self.assign_point_list_dict[kValue] = assign_point_list


    def distribute_example(self,one_assign_point_list):
        all_class = list()
        for example in one_assign_point_list:
            if example.inClass not in all_class:
                all_class.append(example.inClass)
        
        distribute_example_dict = dict()
        for class_No in all_class:
            distribute_example_dict[class_No] = list()
            for example in one_assign_point_list:
                if example.inClass == class_No:
                    distribute_example_dict[class_No].append(example)
        return distribute_example_dict


    def calculate_class_diameter(self, one_class_list):
        tot_diameter_one_class = 0
        outer_iter_list = copy.deepcopy(one_class_list)
        #inner_iter_list = copy.deepcopy(one_class_list)
        for item_outer in outer_iter_list:
            inner_iter_list = copy.deepcopy(outer_iter_list)
            main_point = outer_iter_list.pop()
            for item_inner in inner_iter_list:
                tot_diameter_one_class = tot_diameter_one_class + item_outer.distance_between(item_inner.coordinate)
        return tot_diameter_one_class

    def calculate_diameter_one_k(self, one_assign_point_list):
        distribute_example_dict = self.distribute_example(one_assign_point_list)
        tot_diameter = 0
        for key,value in distribute_example_dict.items():
            one_diameter = self.calculate_class_diameter(value)
            tot_diameter = tot_diameter + one_diameter

        average_diameter = tot_diameter/len(distribute_example_dict)
        return average_diameter

    def k_diameter(self):
        self.kMeans_with_different_k()
        k_diameter_dict = dict()
        for key_assign, value_assign in self.assign_point_list_dict.items():
            k_diameter_dict[key_assign] = self.calculate_diameter_one_k(value_assign)
        return k_diameter_dict






    