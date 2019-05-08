import os
class Node:
    def __init__(self,player,list_of_spla_children,list_of_lahsa_children,value,parking_remaining,beds_remaining,pick,tie):
        self.player=player
        self.list_of_spla_children=list_of_spla_children
        self.list_of_lahsa_children = list_of_lahsa_children
        self.value=value
        self.parking_remaining=parking_remaining
        self.beds_remaining = beds_remaining
        self.pick=pick
        self.tie = tie


class Applicant:
    def __init__(self, applicant_id,applicant_sex,applicant_age,applicant_pet,applicant_medical,applicant_car,applicant_license,applicant_days):
        self.applicant_id=applicant_id
        self.applicant_sex=applicant_sex
        self.applicant_age=applicant_age
        self.applicant_pet=applicant_pet
        self.applicant_medical=applicant_medical
        self.applicant_car=applicant_car
        self.applicant_license=applicant_license
        self.applicant_days=applicant_days


def main():
    output = open(os.getcwd() + "/output.txt", "w")
    input_file = open(os.getcwd() + "/input17.txt", "r")
    no_of_beds_in_shelter = int(input_file.readline().strip())
    no_of_spaces_in_parking_lot = int(input_file.readline().strip())

    no_of_applicants_chosen_by_lahsa=int(input_file.readline().strip())
    list_of_applicants_chosen_lahsa=[]
    for applicant in range(no_of_applicants_chosen_by_lahsa):
        list_of_applicants_chosen_lahsa.append(input_file.readline().strip())

    no_of_applicants_chosen_by_spla = int(input_file.readline().strip())
    list_of_applicants_chosen_spla=[]
    for applicant in range(no_of_applicants_chosen_by_spla):
        list_of_applicants_chosen_spla.append(input_file.readline().strip())

    no_of_applicants = int(input_file.readline())
    list_of_applicants_considered_for_lahsa = {}
    list_of_applicants_considered_for_spla={}


    beds={'0':no_of_beds_in_shelter,'1':no_of_beds_in_shelter,'2':no_of_beds_in_shelter,'3':no_of_beds_in_shelter,'4':no_of_beds_in_shelter,'5':no_of_beds_in_shelter,'6':no_of_beds_in_shelter}
    parking={'0':no_of_spaces_in_parking_lot,'1':no_of_spaces_in_parking_lot,'2':no_of_spaces_in_parking_lot,'3':no_of_spaces_in_parking_lot,'4':no_of_spaces_in_parking_lot,'5':no_of_spaces_in_parking_lot,'6':no_of_spaces_in_parking_lot}

    #get list of applicants
    for x in range(no_of_applicants):
        applicant=input_file.readline().strip()
        applicant_id=applicant[0:5]
        applicant_sex=applicant[5]
        applicant_age=int(applicant[6:9])
        applicant_pet = applicant[9]
        applicant_medical = applicant[10]
        applicant_car = applicant[11]
        applicant_license = applicant[12]
        applicant_days=applicant[13:20]
        if not (applicant_id in list_of_applicants_chosen_lahsa) and not (applicant_id in list_of_applicants_chosen_spla):
            if applicant_sex=='F' and applicant_age>17 and applicant_pet=='N':
                applicant = Applicant(applicant_id,applicant_sex,applicant_age,applicant_pet,applicant_medical,applicant_car,applicant_license,applicant_days)
                list_of_applicants_considered_for_lahsa[applicant_id]=applicant
            if applicant_car=='Y' and applicant_license=='Y' and applicant_medical=='N':
                applicant = Applicant(applicant_id,applicant_sex,applicant_age,applicant_pet,applicant_medical,applicant_car,applicant_license,applicant_days)
                list_of_applicants_considered_for_spla[applicant_id]=applicant

        elif applicant_id in list_of_applicants_chosen_lahsa:
            for x in range(7):
                if applicant_days[x] == '1':
                    beds[str(x)]-=1

        elif applicant_id in list_of_applicants_chosen_spla:
            for x in range(7):
                if applicant_days[x] == '1':
                    parking[str(x)]-=1



    def dfs():
        node=Node("spla",list_of_applicants_considered_for_spla,list_of_applicants_considered_for_lahsa,0,parking,beds,0,0)
        stack = []
        leaf_node_list =[]
        stack.append(node)
        count=0
        while len(stack) != 0:
            current_node = stack.pop()
            count=count+1
            pick=current_node.pick
            if (current_node.player == "spla"):
                list_of_children = current_node.list_of_spla_children
            else:
                list_of_children = current_node.list_of_lahsa_children

            if len(list_of_children)==0:
                lasha_sum=0
                spla_sum=0
                if len(current_node.list_of_lahsa_children)!=0:
                    temp_parking_list = dict(current_node.beds_remaining)
                    for x in current_node.list_of_lahsa_children:
                        value=current_node.list_of_lahsa_children.get(x)
                        for x in range(7):
                            if value.applicant_days[x] == '1' and possible==1:
                                temp_parking_list[str(x)] -= 1
                                lasha_sum=lasha_sum+1
                                if temp_parking_list[str(x)]<0:
                                    temp_parking_list = dict(current_node.beds_remaining)
                                    possible=0
                                    value=0
                    current_node.value=current_node.value+lasha_sum
                    leaf_node_list.append(current_node)
                if len(current_node.list_of_spla_children)!=0:
                    temp_parking_list = dict(current_node.parking_remaining)
                    for x in current_node.list_of_spla_children:
                        value=current_node.list_of_spla_children.get(x)
                        for x in range(7):
                            if value.applicant_days[x] == '1' and possible==1:
                                temp_parking_list[str(x)] -= 1
                                spla_sum=spla_sum+1
                                if temp_parking_list[str(x)]<0:
                                    temp_parking_list = dict(current_node.parking_remaining)
                                    possible=0
                                    value=0
                    current_node.value=current_node.value+spla_sum
                    leaf_node_list.append(current_node)
                if len(current_node.list_of_spla_children) == 0 and len(current_node.list_of_lahsa_children)==0:
                    leaf_node_list.append(current_node)

            else:
                for each_child in list_of_children:
                    each_value=list_of_children.get(each_child)
                    if(current_node.player=="spla"):
                        temp_parking_list = dict(current_node.parking_remaining)
                        temp_spla_list=dict(current_node.list_of_spla_children)
                        temp_lahsa_list=dict(current_node.list_of_lahsa_children)
                        possible = 1
                        value=0
                        for x in range(7):
                            if each_value.applicant_days[x] == '1' and possible==1:
                                temp_parking_list[str(x)] -= 1
                                value=value+1
                                if temp_parking_list[str(x)]<0:
                                    temp_parking_list = dict(current_node.parking_remaining)
                                    possible=0
                                    value=0
                        if each_child in temp_spla_list:
                            del temp_spla_list[each_child]
                        if each_child in temp_lahsa_list:
                            del temp_lahsa_list[each_child]
                        if count==1:
                            pick=each_child
                        node = Node("lahsa", temp_spla_list,
                                        temp_lahsa_list,current_node.value+value, temp_parking_list, current_node.beds_remaining,pick,each_child)
                        stack.append(node)
                    else:
                        temp_beds_list = dict(current_node.beds_remaining)
                        temp_spla_list = dict(current_node.list_of_spla_children)
                        temp_lahsa_list = dict(current_node.list_of_lahsa_children)
                        possible = 1
                        value=0
                        for x in range(7):
                            if each_value.applicant_days[x] == '1' and possible == 1:
                                temp_beds_list[str(x)] -= 1
                                value = value + 1
                                if temp_beds_list[str(x)] < 0:
                                    temp_beds_list = dict(current_node.beds_remaining)
                                    possible = 0
                                    value = 0
                        if each_child in temp_spla_list:
                            del temp_spla_list[each_child]
                        if each_child in temp_lahsa_list:
                            del temp_lahsa_list[each_child]
                        if count==1:
                            pick=each_child
                        node = Node("spla", temp_spla_list,
                                        temp_lahsa_list,current_node.value, current_node.parking_remaining, temp_beds_list,pick,each_child)
                        stack.append(node)

        max=0
        applicant=0
        tie=0
        for x in leaf_node_list:
            if x.value > max:
                max=x.value
                applicant=x.pick
                tie=x.tie
            elif x.value==max:
                if x.tie<tie:
                    tie=x.tie
                    applicant = x.pick
                elif x.tie==tie:
                    if x.pick<applicant:
                        applicant=x.pick
                    else:
                        applicant=applicant

        output.write(str(applicant))


    dfs()
    input_file.close()
    output.close()


if __name__ == "__main__":
        main()

