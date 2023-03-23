import time
from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import numpy as np  # mathematical calculation
import pandas as pd  # manipulating the csv data
from anytree import Node  # node classes for graph generation
from anytree.exporter import DotExporter  # node structure export to img

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

start_time = time.time()

# data needs to be arranged in a certain way before importing
# 2 level of headers are needed
train_data_m = pd.read_csv(filename, sep=";",
                           header=[0, 1])  # importing the dataset


def get_conclusion_header(train_data):
    h = train_data.columns.get_level_values(0)
    h_arr = np.array(h)
    return h_arr[len(h_arr) - 1]


def get_headers_lvl0(train_data):  # get headers in dataset
    h = train_data.columns.get_level_values(0)
    h_arr = np.array(h)
    h_arr = np.unique(h_arr)
    conclusion = get_conclusion_header(train_data)
    h_arr = h_arr[h_arr != conclusion]
    return h_arr


def get_parent_classes(string):  # get node path
    deleted = []
    s = str(string)
    s = s[7:len(s) - 54]
    split = s.split("/")
    for s in split:
        sub = s.split(":")[1]
        deleted.append(sub)
    return deleted


def get_conclusions(train_data):  # get conclusions in dataset
    conclusion = get_conclusion_header(train_data)
    c = train_data[conclusion].columns
    c_array = np.array(c)
    return c_array


def set_color_shape(node):  # set node attributes
    attrs = []
    attrs += [f'color={node.color}'] if hasattr(node, 'color') else []
    attrs += [f'shape={node.shape}'] if hasattr(node, 'shape') else []
    return ', '.join(attrs)


def calc_total_entropy(train_data):  # get total entrophy
    total_row = train_data.shape[0]  # number of observations
    total_entr = 0
    class_list = get_conclusions(train_data)  # conclusions list
    conclusion = get_conclusion_header(train_data)
    for c in class_list:  # for each conclusion in the dataset
        total_class_count = sum(train_data[conclusion][c] == 1)  # number of conclusion
        if total_class_count > 0:
            total_class_entr = - (total_class_count / total_row) * np.log2(
                total_class_count / total_row)  # entrophy for conclusion c
        else:
            total_class_entr = 0
        total_entr += total_class_entr  # entrophy for the whole dataset
    return total_entr


def max_gain(train_data):  # get maximum gain
    I = calc_total_entropy(train_data)
    headers = get_headers_lvl0(train_data)
    class_list = get_conclusions(train_data)
    conclusion = get_conclusion_header(train_data)
    # total_I = 0
    max_gain = 0
    for h1 in headers:
        for h2 in train_data[h1].columns:
            IE = 0
            for numb in [0, 1]:
                total_I = 0  # I+ and I-
                for c in class_list:
                    rows = train_data[h1][h2].shape[0]  # number of observations
                    s1 = (train_data[h1][h2] == numb)  # negate/approve condition h2
                    nominative = sum(s1)  # number of negated/approved condition h2
                    s2 = (train_data[conclusion][c] == 1)  # rows with conclusion c
                    numerator = sum(s1 & s2)  # number of negated/approved condition and conclusion c
                    if numerator == 0:
                        entrophy_class = 0
                    else:
                        entrophy_class = - (numerator / nominative) * np.log2(
                            numerator / nominative)
                    total_I += entrophy_class  # I
                IE += (nominative / rows) * total_I
            if I - IE > max_gain:
                max_gain = I - IE
                max_h1 = h1
                max_h2 = h2
    return max_h1, max_h2


def del_cls(train_data, deleted_classes):  # get all conclusions in path
    for h1 in get_headers_lvl0(train_data):
        for h2 in train_data[h1].columns:
            if h2 in deleted_classes:
                train_data = train_data.drop(h2, axis=1, level=1)
                if len(train_data[h1].columns) == 1:
                    arr = np.array(train_data[h1].columns)
                    dele = arr[0]
                    train_data = train_data.drop(dele, axis=1, level=1)
    return train_data


def split_table(train_data):
    split_class = max_gain(train_data)
    table_split_1 = train_data[
        train_data[split_class[0]][split_class[1]] == 1]  # table with approved splitting condition
    table_split_0 = train_data[
        train_data[split_class[0]][split_class[1]] == 0]  # table with negated splitting condition
    return table_split_0, table_split_1


def check_purity(train_data):  # check table purity
    conclusion = get_conclusion_header(train_data)
    rows = len(train_data.index)
    conclusion_list = get_conclusions(train_data)
    for c in conclusion_list:
        s2 = sum(train_data[conclusion][c] == 1)
        if s2 == rows:
            return "konkluzja", c  # if pure
    return 0  # if not pure


table_and_node = []
temp = []
row = 0
alph = 97
root = Node(str(row) + ". " + max_gain(train_data_m)[0] + ": " + max_gain(train_data_m)[1], shape="rectangle",
            weight="tak", color="blue")  # tree root
table_and_node.append([train_data_m, root])  # starting table and root

while (len(table_and_node) > 0):  # split tables untill found purity
    row += 1
    alph = 97
    for c in table_and_node:  # split table and check for purity
        splitted = split_table(c[0])
        classes = get_parent_classes(c[1])  # array of conditions in path
        splitted_0 = del_cls(splitted[0], classes)
        purity_0 = check_purity(splitted_0)

        if purity_0 == 0:  # if table is not pure add another condition to node structure
            name_parts = max_gain(splitted_0)
            if alph < 122:
                name = str(row) + chr(alph) + ". " + name_parts[0] + ": " + name_parts[1]
            else:
                name = str(row) + chr(alph - 97) + ". " + name_parts[0] + " : " + name_parts[1]
            node = Node(name, parent=c[1], weight=" nie", shape="rectangle", color="darkorange")
            temp.append([splitted_0, node])
        else:  # if table is pure add conclusion to node structure
            name_parts = purity_0
            if alph < 122:
                name = str(row) + chr(alph) + ". " + name_parts[0] + ": " + name_parts[1]
            else:
                name = str(row) + chr(alph - 97) + ". " + name_parts[0] + " : " + name_parts[1]

            node = Node(name, parent=c[1], weight=" nie", color="darkgreen")
        alph += 1
        splitted_1 = del_cls(splitted[1], classes)
        purity_1 = check_purity(splitted_1)
        if purity_1 == 0:
            name_parts = max_gain(splitted_1)
            if alph < 122:
                name = str(row) + chr(alph) + ". " + name_parts[0] + ": " + name_parts[1]
            else:
                name = str(row) + chr(alph - 97) + ". " + name_parts[0] + " : " + name_parts[1]

            node = Node(name, parent=c[1], weight=" tak", shape="rectangle", color="darkorange")
            temp.append([splitted_1, node])
        else:
            name_parts = purity_1
            if alph < 122:
                name = str(row) + chr(alph) + ". " + name_parts[0] + ": " + name_parts[1]
            else:
                name = str(row) + chr(alph - 97) + ". " + name_parts[0] + " : " + name_parts[1]

            node = Node(name, parent=c[1], weight=" tak", color="darkgreen")
        alph += 1
    table_and_node = temp
    temp = []

DotExporter(root).to_dotfile("tree.dot")

try:
    DotExporter(root, nodeattrfunc=set_color_shape,
                edgeattrfunc=lambda parent, child: "style=bold,label=%s" % (child.weight or "?")).to_picture(
        "ID3.png")  # export graph to ID3.png
except:
    print("Nie udało się wyeksportować drzewka do .png")

print("Exec time: --- %s seconds ---" % round((time.time() - start_time), 2))
