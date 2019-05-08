import os
import copy
import numpy as np

def main():
    output = open(os.getcwd() + "/output.txt", "w")
    input_file = open(os.getcwd() + "/input0.txt", "r")

    size = int(input_file.readline().strip())
    no_of_cars= int(input_file.readline().strip())
    no_of_obstacles= int(input_file.readline().strip())

    list_of_obstacles = []
    for obstacles in range(no_of_obstacles):
        list_of_obstacles.append(input_file.readline().strip())

    list_of_start_locations = []
    for start in range(no_of_cars):
        list_of_start_locations.append(input_file.readline().strip())

    list_of_end_locations = []
    for end in range(no_of_cars):
        list_of_end_locations.append(input_file.readline().strip())

    reward=-1.0
    gamma=0.9
    correct_direction_probability=0.7
    wrong_direction_probability=0.1

    def TurnLeftLeft(move,direction):
        if direction == 'N':
            if move[0]==size-1:
                return move
            return (move[0]+1,move[1])
        if direction == 'S':
            if move[0]==0:
                return move
            return (move[0]-1,move[1])
        if direction == 'E':
            if move[1]==0:
                return move
            return (move[0],move[1]-1)
        if direction == 'W':
            if move[1]==size-1:
                return move
            return (move[0],move[1]+1)


    def TurnLeft(move,direction):
        if direction == 'N':
            if move[1]==0:
                return move
            return (move[0],move[1]-1)
        if direction == 'S':
            if move[1]==size-1:
                return move
            return (move[0],move[1]+1)
        if direction == 'E':
            if move[0]==0:
                return move
            return (move[0]-1,move[1])
        if direction == 'W':
            if move[0]==size-1:
                return move
            return (move[0]+1,move[1])

    def TurnRight(move,direction):
        if direction == 'N':
            if move[1]==size-1:
                return move
            return (move[0],move[1]+1)
        if direction == 'S':
            if move[1]==0:
                return move
            return (move[0],move[1]-1)
        if direction == 'E':
            if move[0]==size-1:
                return move
            return (move[0]+1,move[1])
        if direction == 'W':
            if move[0]==0:
                return move
            return (move[0]-1,move[1])

    def North(c,r ,Utility):
        if r==0:
            return Utility[r][c]
        return Utility[r-1][c]


    def South(c, r, Utility):
        if r==size-1:
            return Utility[r][c]
        return Utility[r+1][c]


    def East(c, r, Utility):
        if c==size-1:
            return Utility[r][c]
        return Utility[r][c+1]


    def West(c, r, Utility):
        if c==0:
            return Utility[r][c]
        return Utility[r][c-1]

    def calculateMaximum(maximum):
        m=maximum[0]
        max_index=0
        for index in range(4):
            if maximum[index] > m:
                m=maximum[index]
                max_index=index
        return max_index

    def calculateUtilityPrime(c,r,UtilityPrime,Reward,Utility,endr,endc):
        if c == endc and r == endr:
                UtilityPrime[r][c] = Reward[r][c]
        else:
            maximum = [0, 0, 0, 0]
            north = North(c, r, Utility)
            south = South(c, r, Utility)
            east = East(c, r, Utility)
            west = West(c, r, Utility)
            maximum[
                0] = north * correct_direction_probability + south * wrong_direction_probability + east * wrong_direction_probability + west * wrong_direction_probability

            maximum[
                1] = south * correct_direction_probability + east * wrong_direction_probability + west * wrong_direction_probability + north * wrong_direction_probability

            maximum[
                2] = east * correct_direction_probability + west * wrong_direction_probability + north * wrong_direction_probability + south * wrong_direction_probability

            maximum[
                3] = west * correct_direction_probability + north * wrong_direction_probability + south * wrong_direction_probability + east * wrong_direction_probability

            maxi = calculateMaximum(maximum)

            UtilityPrime[r][c] = Reward[r][c] + gamma * maximum[maxi]

    def calculatePol(r,c,Policy,PolicyDirection,Utility):
        maximum = [0, 0, 0, 0]
        maximum[0] = North(c, r, Utility)
        maximum[1] = South(c, r, Utility)
        maximum[2] = East(c, r, Utility)
        maximum[3] = West(c, r, Utility)
        maxi = calculateMaximum(maximum)
        if maxi == 0:
            if r==0:
                Policy[r][c] = (r, c)
                PolicyDirection[r][c] = 'N'
            else:
                Policy[r][c] = (r - 1, c)
                PolicyDirection[r][c] = 'N'
        elif maxi == 1:
            if r==size-1:
                Policy[r][c] = (r, c)
                PolicyDirection[r][c] = 'S'
            else:
                Policy[r][c] = (r + 1, c)
                PolicyDirection[r][c] = 'S'
        elif maxi == 2:
            if c == size - 1:
                Policy[r][c] = (r, c)
                PolicyDirection[r][c] = 'E'
            else:
                Policy[r][c] = (r, c + 1)
                PolicyDirection[r][c] = 'E'
        elif maxi == 3:
            if c==0:
                Policy[r][c] = (r, c)
                PolicyDirection[r][c] = 'W'
            else:
                Policy[r][c] = (r, c - 1)
                PolicyDirection[r][c] = 'W'

    def calculatePolicy(r,c):
        UtilityPrime = [[0.0] * size for i in range(size)]
        Reward = [[reward] * size for i in range(size)]
        PolicyDirection = [[0.0] * size for i in range(size)]
        Policy = [[0.0] * size for i in range(size)]

        for obstacles in list_of_obstacles:
            data = obstacles.split(',')
            Reward[int(data[1])][int(data[0])] = Reward[int(data[1])][int(data[0])] + (-100.0)

        Reward[r][c] = Reward[r][c] + 100.0
        delta=1
        while delta>=(0.1 * (1 - gamma) / gamma):
            delta = 0.0
            Utility = copy.deepcopy(UtilityPrime)
            for r1 in range(size):
                for c1 in range(size):
                    calculateUtilityPrime(c1, r1, UtilityPrime, Reward,Utility,r,c)
                    if (abs(UtilityPrime[r1][c1] - Utility[r1][c1])) > delta:
                        delta = abs(UtilityPrime[r1][c1] - Utility[r1][c1])
                    calculatePol(r1,c1,Policy, PolicyDirection, Utility)
        return Reward, Policy, PolicyDirection

    for i in range(no_of_cars):
        data=list_of_end_locations[i]
        end_coordinates=data.split(',')
        Reward,Policy, PolicyDirection=calculatePolicy(int(end_coordinates[1]),int(end_coordinates[0]))
        data = list_of_start_locations[i]
        start_coordinates = data.split(',')
        average_sum=0.0
        for j in range(10):
            pos=(int(start_coordinates[1]),int(start_coordinates[0]))
            np.random.seed(j)
            swerve = np.random.random_sample(1000000)
            k = 0
            sum=0.0
            while pos[0]!=int(end_coordinates[1]) or pos[1]!=int(end_coordinates[0]) :
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            move = TurnLeftLeft(pos,PolicyDirection[pos[0]][pos[1]])
                            if k != 0:
                                sum = sum + Reward[pos[0]][pos[1]]
                            pos = move
                        else:
                            move = TurnRight(pos,PolicyDirection[pos[0]][pos[1]])
                            if k != 0:
                                sum = sum + Reward[pos[0]][pos[1]]
                            pos = move
                    else:
                        move = TurnLeft(pos,PolicyDirection[pos[0]][pos[1]])
                        if k != 0:
                            sum = sum + Reward[pos[0]][pos[1]]
                        pos = move
                else:
                    if k!=0:
                        sum = sum + Reward[pos[0]][pos[1]]
                    pos = Policy[pos[0]][pos[1]]
                k=k+1
            if k==0 and pos[0]==int(end_coordinates[1]) and pos[1]==int(end_coordinates[0]) :
                sum=sum+100
            else:
                sum = sum + Reward[pos[0]][pos[1]]
            average_sum=average_sum+sum
        average=np.floor(average_sum/10.0)
        output.write(str(int(average))+"\n")

if __name__ == "__main__":
        main()

