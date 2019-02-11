"""
10/20/2018
Author: Amol Gaikwad

Decision Tree trainer

"""
__author__ = 'Amol Gaikwad'

import sys
import math
import warnings
import pandas as pd

def main():
    """
        Main Program
        Handle command line arguments.

        :param : Command line arguments
        :argv[1]: CSV file to be loaded

        :return: None
    """
    warnings.filterwarnings("ignore")
    # Read number of arguments
    noofargs = len(sys.argv)

    # Check for invalid number of arguments
    if (noofargs != 2):
        print("Invalid number of arguments")
    else:
        inp_file = sys.argv[1]
        # Get data frame
        data = preprocess(inp_file)
        print("Classifier HW_05_Gaikwad_Amol_Classifier.py generated")
        # Emit classifier header
        file = write_file_header()
        tabspace = 1
        # Build decision tree
        build_tree(data, file, tabspace)
        # Emit classifier trailer
        write_file_trailer(file)


def preprocess(file):
    """
           Preprocess input file data

           :param :
            file: Input csv file

           :return:
            data: preprocessed data

    """
    data = pd.read_csv(file)
    return data

def write_file_header():
    """
       Emit classifier header

       :param :
        None

       :return:
        data: written file

    """
    file = open("HW_05_Gaikwad_Amol_Classifier.py","w+")
    file.write("# Generated classifier file. Few indentations need to be corrected.\n")
    file.write("__author__ = 'Amol Gaikwad'\n")
    file.write("import pandas as pd\n")
    file.write('target_class = ["Cupcake", "Muffin"]\n')
    file.write("\n")
    file.write("def tree(attr):\n")

    return file

def write_file_trailer(file):
    """
       Emit classifier trailer

       :param :
        file

       :return:
        None

    """
    # Add main function to calculate accuracy and output my classification data
    str = """
    def main():
    csv_data = pd.read_csv("Recipes_For_VALIDATION_2181_RELEASED_v202.csv")
    len_data = len(csv_data)
    f = open("HW_05_Gaikwad_Amol_MyClassifications.csv", "w+")

    for x in range(0, len_data):
        res = tree(csv_data.iloc[x,1:])
        if res!=None:
            f.write(res)
            f.write()

    csv_data = pd.read_csv("Recipes_For_Release_2181_v202.csv")
    len_data = len(csv_data)
    # fp = open("HW_05_Gaikwad_Amol_Accuracy.csv", "w+")

    correct_hits = 0
    total = len_data
    for x in range(0, len_data):
        res = tree(csv_data.iloc[x, 1:])
        if res != None:
            if res == csv_data["Type"].tolist()[x]:
                correct_hits = correct_hits +1

    accuracy = (correct_hits / total) * 100
    print("Output of validation file generated in HW_05_Gaikwad_Amol_MyClassifications.csv file")
    print("Accuracy of training data is "+str(accuracy)+" percent")


if __name__ == '__main__':
    main()
    """
    file.write(str)

def write_file_condition(data, file, attr, threshold, tabspace):
    """
       Write condition of decision tree

       :param :
        data: data from which tree is to be built
        file: file to write decision tree to
        attr: attribute name
        threshold: threshold value
        tabspace: number of tab spaces
        criteria: specify criteria

       :return:
        target_class: class label
        tabspace: tab spaces

    """
    columnNames = list(data.head(0))
    attr_idx = [idx for idx in range(0, len(columnNames)) if columnNames[idx] == attr]

    tabstr = "\t" * tabspace

    # If condition of decision tree
    file.write(tabstr+"if float(attr["+str(attr_idx[0])+"]) <"+str(threshold)+":\n")
    print(tabstr + "if " + attr + " < " + str(threshold) + ":\n")


    return file, tabspace

def build_tree(data, file, tabspace):
    """
       Build decision tree

       :param :
        data: data from which tree is to be built
        file: file to write decision tree to
        tabspace: number of tab spaces

       :return:
        target_class: class label
        tabspace: tab spaces

    """
    target_class, is_stop = stopping_criteria(data["Type"])
    if is_stop:
        # Stopping criteria met
        file.write("\t" * tabspace)
        if target_class == "Cupcake":
            target_idx = 0
        elif target_class == "Muffin":
            target_idx = 1
        # Write target class to classifier file
        file.write("return target_class["+str(target_idx)+"]")
        print("return "+target_class)
        file.write("\n")
        tabspace = tabspace - 1
        return target_class, tabspace
    else:
        # Calculate weighted gini, threshold and attribute
        mix_gini, threshold, attr = get_gini_index(data)

        # Write decision tree condition
        file, tabspace = write_file_condition(data,file,attr,threshold, tabspace)

        tabspace = tabspace + 1
        # Split data into left half
        left_data = get_data_frame(data, attr, threshold, "lower")
        # Split data into right half
        right_data = get_data_frame(data, attr, threshold, "higher")

        # Recursively call for left half
        class_left,tabspace = build_tree(left_data, file, tabspace)
        file.write("\t" * tabspace + "else:\n")
        print("\t" * tabspace + "else:\n")
        # Recursively call for right half
        tabspace = tabspace + 1
        class_right,tabspace = build_tree(right_data, file, tabspace)

        return None,tabspace

def get_data_frame(data, attr, threshold, criteria):
    """
       Get data frames from data

       :param :
        data: data from which frames are to be made
        attr: attribute name
        threshold: threshold value
        criteria: specify getting data lower than or greater than threshold

       :return:
        data: data frame

    """
    if criteria == "lower":
        # Get data frame of values lower than threshold
        filter_data = data[attr] < threshold
        data = data[filter_data]
    elif criteria == "higher":
        # Get data frame of values higher than threshold
        filter_data = data[attr] >= threshold
        data = data[filter_data]

    return data

def get_gini_index(data):
    """
       Get weighted gini for data

       :param :
        data: data whose gini index is to be found

       :return:
        best_mix_gini: weighted gini
        best_threshold: best threshold value
        best_attribute: best attribute value

    """
    # Skip first target class column
    col_data = data.iloc[:, 1:]
    best_mix_gini = math.inf
    best_threshold = math.inf
    best_attribute = ""
    # Iterate over all attributes
    for attr in col_data.columns:
        threshold_unique = []
        # Get unique threshold values
        for val in data[attr]:
            if val not in threshold_unique:
                threshold_unique.append(float(val))

        # Iterate over all thresholds
        for threshold in threshold_unique:
            list_lowerthreshold = []
            list_higherthreshold = []
            target_lowerthreshold = []
            target_higherthreshold = []

            for idx in range(0, len(data[attr])):
                val = data[attr].tolist()[idx]
                if val < threshold:
                    # Append lower than threshold values
                    list_lowerthreshold.append(float(val))
                    # Append target class values for less than threshold
                    target_lowerthreshold.append(data["Type"].tolist()[idx])
                elif val >= threshold:
                    # Append higher than threshold values
                    list_higherthreshold.append(float(val))
                    # Append target class values higher than threshold
                    target_higherthreshold.append(data["Type"].tolist()[idx])


            # Calculate gini for lower values than threshold
            if(len(list_lowerthreshold) !=0):
                try:

                    list_zero_lower = [list_lowerthreshold[idx] for idx in range(0,len(list_lowerthreshold)) if target_lowerthreshold[idx] == "Cupcake"]
                    prob_zero_lower = len(list_zero_lower) / len(list_lowerthreshold)

                    list_one_lower = [list_lowerthreshold[idx] for idx in range(0,len(list_lowerthreshold)) if target_lowerthreshold[idx] == "Muffin"]
                    prob_one_lower = len(list_one_lower) / len(list_lowerthreshold)

                    ginival_lower = 1 - prob_zero_lower ** 2 - prob_one_lower ** 2
                except:
                    ginival_lower = 0
            else:
                ginival_lower = 0

            # Calculate gini for higher values than threshold
            if (len(list_higherthreshold) != 0):

                try:
                    list_zero_higher = [list_higherthreshold[idx] for idx in range(0,len(list_higherthreshold)) if target_higherthreshold[idx] == "Cupcake"]

                    prob_zero_higher = len(list_zero_higher) / len(list_higherthreshold)

                    list_one_higher = [list_higherthreshold[idx] for idx in range(0,len(list_higherthreshold)) if target_higherthreshold[idx] == "Muffin"]

                    prob_one_higher = len(list_one_higher) / len(list_higherthreshold)
                    ginival_higher = 1 - prob_zero_higher ** 2 - prob_one_higher ** 2
                except:
                    ginival_higher = 0
            else:
                ginival_higher = 0





            total_val = len(list_lowerthreshold)+len(list_higherthreshold)


            if total_val!=0:
                # Calclulate weighted gini
                mix_gini_low = len(list_lowerthreshold) * ginival_lower
                mix_gini_high = len(list_higherthreshold) * ginival_higher
                mix_gini = (mix_gini_low + mix_gini_high)/total_val

                if mix_gini < best_mix_gini:
                    # Set best gini, threshold and attribute
                    best_mix_gini = mix_gini
                    best_threshold = threshold
                    best_attribute = attr

    return best_mix_gini, best_threshold, best_attribute

def stopping_criteria(data):
    """
       Stopping criteria for trainer

       :param :
        data: target class data

       :return:
        target_class: class label
        criteria_met: boolean to indicate whether to stop tree generation

    """
    count_muffin = 0
    count_cupcake = 0
    target_class = ""
    criteria_met = False

    for val in data:
        if val == "Cupcake":
            count_cupcake = count_cupcake + 1
        elif val == "Muffin":
            count_muffin = count_muffin + 1

    if count_cupcake >= 0.95 * count_muffin+count_cupcake:
        # Target class is cupcake and criteria met
        target_class = "Cupcake"
        criteria_met = True
    elif count_muffin >= 0.95 * count_muffin+count_cupcake:
        # Target class is muffin and criteria met
        target_class = "Muffin"
        criteria_met = True

    return target_class, criteria_met

if __name__ == '__main__':
    main()