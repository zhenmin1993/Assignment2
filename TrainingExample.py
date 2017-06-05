import math
import copy

class TrainingExample():
    def __init__(self, coordinate, original_coordinate):
        self.coordinate = coordinate
        self.inClass = 0
        self.original_coordinate = original_coordinate


    def change_Class(self,new_class):
        self.inClass = new_class

    def Eculidean(self,point1, point2):
        if len(point1) != len(point2):
            print('two points in different dimension!')

        if len(point1) == len(point2):
            Ecu_distance_temp = 0
            for iter_point in range(len(point1)):
                temp_square = (point1[iter_point] - point2[iter_point]) * (point1[iter_point] - point2[iter_point])
                Ecu_distance_temp = Ecu_distance_temp + temp_square

            Ecu_distance = math.sqrt(Ecu_distance_temp)
            return Ecu_distance

    def distance_between(self, new_coord):
        return self.Eculidean(self.coordinate, new_coord)
        self.Eculidean_distance = self.Eculidean(self.coordinate, new_coord)
