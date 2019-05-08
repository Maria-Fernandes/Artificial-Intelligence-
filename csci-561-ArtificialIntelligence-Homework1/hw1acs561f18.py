import re
import os
def main():
    output_file = open(os.getcwd()+"/output.txt", "w")
    pattern = re.compile("[aAbB]{1},[a-zA-Z]*")
    input_file=open(os.getcwd() + "/input.txt", "r")
    str=""
    for each_line in input_file:
        if pattern.match(each_line):
            words = each_line.split(",")
            location = words[0].strip().capitalize()
            status = words[1].strip().capitalize()
            if status == "Dirty" :
                str+="Suck\n"
            elif location == "A" and status == "Clean":
                str+="Right\n"
            elif location == "B" and status == "Clean":
                str+="Left\n"
    output_file.write(str.strip())
    input_file.close()
    output_file.close()
if __name__ == "__main__":
    main()
