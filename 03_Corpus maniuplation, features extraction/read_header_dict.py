import csv
import os

dicionary_input = os.getcwd() + "/header_dictionary.csv"

dict = {}
csv_file = open(dicionary_input, encoding='utf-8')
open_file = csv.reader(csv_file, delimiter=";")
for line in open_file:
    if len(line) == 0:
        pass
    else:
        dict[line[0]] = line[1]

#print dict
for k in dict:
    print(k, ": ", dict[k])