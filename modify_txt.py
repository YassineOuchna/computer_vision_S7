import os

file = open("annotations.txt", "r")
new_file = open("annotations_gray.txt", "a")
for line in file.readlines():
    list = line.split("\\")
    list[0] += "_gray"
    ch = ""
    for elem in list:
        if elem == list[-1]:
            ch += elem
        else:
            ch += elem + "\\"
    new_file.write(ch)
file.close()
new_file.close()
