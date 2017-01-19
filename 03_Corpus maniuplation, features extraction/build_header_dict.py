import os
import csv

books_path = os.getcwd() + "/books"

header_dict = {}

list = []
for root, dirs, files in os.walk(books_path):
    for file in files:
        if file.endswith(("_h.txt")):
            current_file_path = os.path.join(root, file)
            # print(file)
            f = open(current_file_path)
            lines = f.readlines()
            for l in lines:
                pass
            # print(l)
            # split last line by tabulator and remove '\n' char from TRUE / FALSE (last item)
            split = l.split(sep="\t")
            split[len(split)-1] = split[len(split)-1].rstrip("\n")

            #build a dictionary
            if split[3] in header_dict and split[0] == header_dict[split[3]][0]:
                pass
            else:
                header_dict[split[3]] = [*split]

print("Dicitionary size: ", len(header_dict))
for k in header_dict:
    print(k, ": ", header_dict[k])


csv_file = open("header_dictionary.csv", "w", encoding='utf-8')
w = csv.writer(csv_file, delimiter=';')
for key, val in header_dict.items():
    w.writerow([key, val])