import os
from copy import copy, deepcopy

class Node:
    def __init__(self, no_of_police_officers, activity_score,node_matrix):
        self.no_of_police_officers = no_of_police_officers
        self.activity_score = activity_score
        self.node_matrix = node_matrix

    def getNoOfPoliceOfficers(self):
        return self.no_of_police_officers

    def getActivityScore(self):
        return self.activity_score

    def getNodeMatrix(self):
        return self.node_matrix



def main():
    output = open(os.getcwd() + "/output.txt", "w")
    input_file = open(os.getcwd() + "/input2.txt", "r")
    board_dimensions=int(input_file.readline())
    no_of_police_officers=int(input_file.readline())
    no_of_scooters=int(input_file.readline())
    scooter_cost_matrix = [[0 for x in range(board_dimensions)] for y in range(board_dimensions)]

    #setting the scooter positions in a 2 dimensional array
    for each_coordinate in input_file.readlines():
        if each_coordinate.strip():
            coordinates = each_coordinate.strip().split(",")
            scooter_cost_matrix[int(coordinates[0])][int(coordinates[1])] += 1

    def bfs():
        #initialise the first node (no police officers are present)
        node=Node(0,0,scooter_cost_matrix)
        leaf_node_list=[]
        queue=[]
        queue.append(node)
        while len(queue)!=0:
            current_node=queue.pop()
            if current_node.getNoOfPoliceOfficers()==no_of_police_officers :
                leaf_node_list.append(current_node.getActivityScore())
            else:
                #generate all children nodes
                police_officers = current_node.getNoOfPoliceOfficers() + 1
                for x in range(board_dimensions):
                    for y in range(board_dimensions):
                        A = deepcopy(current_node.getNodeMatrix())
                        if A[x][y]!=-1:
                            activity_points=current_node.getActivityScore()+A[x][y]
                            A[x][y] = -1
                            sum=x+y
                            difference=x-y
                            for i in range(board_dimensions):
                                A[x][i] = -1
                                A[i][y] = -1
                                for j in range(board_dimensions):
                                    if i+j==sum or i-j==difference:
                                        A[i][j]=-1
                            node=Node(police_officers,activity_points,A)
                            queue.append(node)
        output.write(str(max(leaf_node_list)))

    if no_of_police_officers==1:
        max_score = 0
        for x in range(board_dimensions):
            for y in range(board_dimensions):
                if scooter_cost_matrix[x][y]>max_score:
                    max_score=scooter_cost_matrix[x][y]
        output.write(str(max_score))
    elif no_of_police_officers>1:
        bfs()
    input_file.close()
    output.close()

if __name__ == "__main__":
    main()