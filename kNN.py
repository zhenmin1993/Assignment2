import math
import copy
#from kMeans import *

class kNN():
    def __init__(self,assign_point_list , new_data):        
        self.new_data = new_data
        self.assign_point_list = assign_point_list

    #Find one nearest neighbor in a list of examples
    def find_least_distance(self, example_list):
        least_distance_example = example_list[0]
        for example in example_list:
            if example.distance_between(self.new_data)<least_distance_example.distance_between(self.new_data):
                least_distance_example = example
        example_list.remove(least_distance_example)
        return least_distance_example

        
    #Find the kNN list 
    def find_kNN(self,NN_num):
        all_example_list = copy.deepcopy(self.assign_point_list)
        NN_list = list()

        while len(NN_list)<NN_num:
            least_distance_example = self.find_least_distance(all_example_list)
            NN_list.append(least_distance_example)

        NN_class_list = list()
        for NN in NN_list:
            NN_class_list.append(NN.inClass)

        return NN_class_list

    #Find majority class number in a NN list
    def find_Majority(self, NN_list):
        SimilarDict = dict()
        for item in NN_list:
            if item not in SimilarDict.keys():
                SimilarDict[item] = 1
            if item in SimilarDict.keys():
                SimilarDict[item] = SimilarDict[item] + 1

        MajorClass = 0
        MajorCount = 0
        for key_similar, value_similar in SimilarDict.items():
            if value_similar > MajorCount:
                MajorClass = key_similar
        return MajorClass

    #Get the final class of the new input
    def AssignClass(self, NN_num):
        return self.find_Majority(self.find_kNN(NN_num))

