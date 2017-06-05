from DataRead import *
from TrainingExample import *
import math
import copy

class kMeans():
    def __init__(self, cluster_num, data_list, TrainingExample_num):
        self.cluster_num = cluster_num
        self.average_point_list = list()
        self.assign_point_list = list()
        self.SubstationInstanceList = data_list
        self.TE_num = TrainingExample_num


    #Initiate every traning example and put them in a list
    def init_assignpoint_list(self):
        assign_point_list = list()

        for iter_traning in range(self.TE_num):
            coord = list()
            for SubstationInstance in self.SubstationInstanceList:
                coord.append(SubstationInstance.VoltageList[iter_traning])
                coord.append(SubstationInstance.AngleList[iter_traning])

            oneExample = TrainingExample(coord)
            assign_point_list.append(oneExample)
        return assign_point_list

    #Initaite every centroids, take 4 training examples       
    def init_avg_point_list(self):
        assign_point_list = self.init_assignpoint_list()
        num = 0
        for iter_cluster_num in range(self.cluster_num):
            coord = list()
            num = num + iter_cluster_num+1
            coord = assign_point_list[num].coordinate
            self.average_point_list.append(coord) 

    #Compute the distance between every training example and every centroids 
    def compute_distance(self):
        assign_point_list = self.init_assignpoint_list()
        distance_list = list()
        for num in range(len(self.average_point_list)):
            distance_list.append(list())

        for iter_point in range(self.TE_num):
            one_point = assign_point_list[iter_point]
            for iter_avg_point in range(len(self.average_point_list)):
                one_distance = one_point.distance_between(self.average_point_list[iter_avg_point])
                distance_list[iter_avg_point].append(one_distance)
        return distance_list

    
    #According to the distance between every training example and every centroid point
    #Assign them to the nearest centroids  
    def assign_point(self,distance_list):
        assign_point_list = self.init_assignpoint_list()
        self.assign_point_list = copy.deepcopy(assign_point_list)
        for iter_distance in range(len(distance_list[0])):
            least_distance = distance_list[0][iter_distance]
            #least_distance_point = 0
            for iter_cluster_num in range(self.cluster_num):
                new_distance = distance_list[iter_cluster_num][iter_distance]
                if least_distance>new_distance:
                    self.assign_point_list[iter_distance].change_Class(iter_cluster_num)
                    #least_distance_point = iter_cluster_num
                    least_distance = copy.deepcopy(new_distance)
            #assign_point_list.append(least_distance_point)

        #return assign_point_list

    #calculate the sum of two coordinate
    def add_coordinate_calculate(self,coord1, coord2):
        if coord1 == None or coord2 ==None:
            return coord1

        else: 
            if len(coord1) != len(coord2):
                print('two points in different dimension!')

            if len(coord1) == len(coord2):
                new_coord = list()
                for iter_coord in range(len(coord1)):
                    new_coord.append(coord1[iter_coord] + coord2[iter_coord]) 
                #new_coord = copy.deepcopy(coord1)
                return new_coord

    #calculate the coordinate of centroids
    def avg_coordinate_calculate(self,coord, point_num):
        avg_coord = list()
        if point_num != 0:
            for iter_coord in range(len(coord)):
                avg_coord.append(coord[iter_coord]/point_num) 

            return avg_coord


    #A function to calculate the coordinate of centroids and update the centroids list (self.average_point_list)
    def new_average_point_list(self):
        self.average_point_list = list()
        for iter_cluster_num in range(self.cluster_num):
            new_coordinate = list()
            for item in range(2*len(self.SubstationInstanceList)):
                new_coordinate.append(0)
            point_num = 0
            for iter_assign in range(len(self.assign_point_list)):
                if iter_cluster_num == self.assign_point_list[iter_assign].inClass:
                    one_coord = self.assign_point_list[iter_assign].coordinate
                    #print(len(one_coord))
                    #print(len(new_coordinate))
                    new_coordinate = self.add_coordinate_calculate(new_coordinate, one_coord)
                    point_num = point_num +1
                    #print(point_num)
            if point_num != 0:
                one_tot_coord = copy.deepcopy(new_coordinate)
                one_avg_coord = self.avg_coordinate_calculate(one_tot_coord,point_num)
                self.average_point_list.append(one_avg_coord)

    #Calculate the total cost of the output
    def cost_calculate(self):
        tot_cost = 0
        for iter_cluster_num in range(self.cluster_num):
            avg_point = self.average_point_list[iter_cluster_num]
            for iter_assign in range(len(self.assign_point_list)):
                if iter_cluster_num == self.assign_point_list[iter_assign].inClass:
                    #one_coord = self.assign_point_list[iter_assign].coordinate
                    one_cost = self.assign_point_list[iter_assign].distance_between(avg_point) * self.assign_point_list[iter_assign].distance_between(avg_point)
                    tot_cost = tot_cost + one_cost
        return tot_cost

    #Main function of kMeans Clustering
    def kMean_Algorithm(self):
        self.init_avg_point_list()
        new_tot_cost = 0
        tot_cost = 100
        while True:
            if new_tot_cost == tot_cost:break
            if new_tot_cost != tot_cost: 
                tot_cost = copy.deepcopy(new_tot_cost)               
                distance_list = self.compute_distance()
                self.assign_point(distance_list)
                self.new_average_point_list()
                new_tot_cost = self.cost_calculate()
                #print(new_tot_cost)
        return self.assign_point_list