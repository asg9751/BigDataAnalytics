"""
09/29/2018
Author: Amol Gaikwad

This program calculates and plots the impurity measures such as misclassification errors, gini index and entropy
Vs threshold speed

"""
__author__ = 'Amol Gaikwad'

import sys
import csv
import math
import warnings
import matplotlib.pyplot as mplot

def main():
    """
        Main Program
        Handle command line arguments. Calculate and plot misclassification errors, gini index and entropy.

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
        file = sys.argv[1]

        # Preprocess the input file
        speedlist, want_to_speed = preprocess(file)

        # Set bin size
        bin_size = 1

        # Round the speed data
        speedlist = [round(float(speed)/bin_size)*bin_size for speed in speedlist]

        # Compute impurity measures
        classerror_lower, gini_lower, entropy_lower, mix_classerror, mix_gini, mix_entropy, threshold_list = get_impurity_measures(speedlist, want_to_speed)

        # Plot cost functions vs threshold
        plotdata(classerror_lower, gini_lower, entropy_lower, threshold_list)

        # Plot mixed cost functions vs threshold
        plotmixdata(mix_classerror, mix_gini, mix_entropy, threshold_list)

def get_impurity_measures(data, want_to_speed):
    """
           This method calculates the impurity measures.

           :param :
            data: Input speed data
            want_to_speed: Input data values for drivers wanting to speed

           :return:
            classerror_lower: List of misclassification error for data lower than threshold
            gini_lower: List of gini indexes for data lower than threshold
            entropy_lower: List of entropy for data lower than threshold
            mix_classerror: List of mixed misclassification error
            mix_gini: List of mixed gini indexes
            mix_entropy: List of mixed entropy
            threshold: List of threshold
    """

    # Set threshold minimum range
    threshold_min = 41
    # Set threshold maximum range
    threshold_max = 86

    # list to store misclassification error values
    classerror_lower = []
    classerror_higher = []
    mix_classerror =[]

    # list to store gini index values
    gini_lower = []
    gini_higher = []
    mix_gini =[]

    # list to store entropy values
    entropy_lower = []
    entropy_higher = []
    mix_entropy = []

    # list to store threshold values
    threshold_list = []

    for threshold in range(threshold_min, threshold_max):
        want_to_speed_lowerthreshold = []
        want_to_speed_higherthreshold = []
        # add threshold value to threshold list
        threshold_list.append(threshold)
        for index in range(0, len(data)):
            # Add to list if speed is less than threshold
            if data[index] < threshold:
                want_to_speed_lowerthreshold.append(int(want_to_speed[index]))
            elif data[index] >= threshold:
                want_to_speed_higherthreshold.append(int(want_to_speed[index]))

        # List having want to speed = 0 for data points less than threshold
        list_zero_lower = [point for point in want_to_speed_lowerthreshold if point == 0]
        # List having want to speed = 1 for data points less than threshold
        list_one_lower = [point for point in want_to_speed_lowerthreshold if point == 1]

        # Calculate P(0) for data points less than threshold
        prob_zero_lower = len(list_zero_lower) / len(want_to_speed_lowerthreshold)
        # Calculate P(1) for data points less than threshold
        prob_one_lower = len(list_one_lower) / len(want_to_speed_lowerthreshold)

        # Calculate and add misclassification error for data points less than threshold
        errorval_lower = 1 - max(prob_zero_lower, prob_one_lower)
        classerror_lower.append(errorval_lower)
        # Calculate and add gini index for data points less than threshold
        ginival_lower = 1 - prob_zero_lower ** 2 - prob_one_lower ** 2
        gini_lower.append(ginival_lower)

        try:
            ent_zero_low = (prob_zero_lower * math.log(prob_zero_lower, 2))
            ent_one_low = (prob_one_lower * math.log(prob_one_lower, 2))
            # Calculate and add entropy for data points less than threshold
            ent_total_low = -1 * (ent_zero_low + ent_one_low)
            entropy_lower.append(ent_total_low)
        except:
            # Catch exception when entropy is zero
            ent_total_low = 0
            entropy_lower.append(ent_total_low)

        # List having want to speed = 0 for data points greater than equal to threshold
        list_zero_higher = [point for point in want_to_speed_higherthreshold if point == 0]
        # List having want to speed = 1 for data points greater than equal to threshold
        list_one_higher = [point for point in want_to_speed_higherthreshold if point == 1]

        # Calculate P(0) for data points greater than equal to threshold
        prob_zero_higher = len(list_zero_higher) / len(want_to_speed_higherthreshold)
        # Calculate P(1) for data points greater than equal to threshold
        prob_one_higher = len(list_one_higher) / len(want_to_speed_higherthreshold)

        # Calculate and add misclassification error for data points greater than equal to threshold
        errorval_higher = 1 - max(prob_zero_higher, prob_one_higher)
        classerror_higher.append(errorval_higher)
        # Calculate and add gini index for data points greater than equal to threshold
        ginival_higher = 1 - prob_zero_higher ** 2 - prob_one_higher ** 2
        gini_higher.append(ginival_higher)

        try:
            ent_zero_high = (prob_zero_higher * math.log(prob_zero_higher, 2))
            ent_one_high = (prob_one_higher * math.log(prob_one_higher, 2))
            # Calculate and add entropy for data points greater than equal to threshold
            ent_total_high = -1 * (ent_zero_high + ent_one_high)
            entropy_higher.append(ent_total_high)
        except:
            # Catch exception when entropy is zero
            ent_total_high = 0
            entropy_higher.append(ent_total_high)

        # Compute total number of speed data points
        total_val = len(want_to_speed_lowerthreshold) + len(want_to_speed_higherthreshold)

        # Compute weighted mixed misclassification error
        mix_classerror_low = (len(want_to_speed_lowerthreshold) / total_val) * errorval_lower
        mix_classerror_high = (len(want_to_speed_higherthreshold) / total_val) * errorval_higher
        mix_classerror.append(mix_classerror_low+mix_classerror_high)

        # Compute weighted mixed gini indexes
        mix_gini_low = (len(want_to_speed_lowerthreshold) / total_val) * ginival_lower
        mix_gini_high = (len(want_to_speed_higherthreshold) / total_val) * ginival_higher
        mix_gini.append(mix_gini_low + mix_gini_high)

        # Compute weighted mixed entropy
        mix_entropy_low = (len(want_to_speed_lowerthreshold) / total_val) * ent_total_low
        mix_entropy_high = (len(want_to_speed_higherthreshold) / total_val) * ent_total_high
        mix_entropy.append(mix_entropy_low + mix_entropy_high)


    return classerror_lower, gini_lower, entropy_lower, mix_classerror, mix_gini, mix_entropy, threshold_list

def plotdata(classerror, gini, entropy, threshold):
    """
           Displays the plot for impurity measures vs threshold

           :param :
            classerror: List of misclassification error
            gini: List of gini indexes
            entropy: List of entropy
            threshold: List of threshold

           :return:
            None
    """
    mplot.figure(figsize=[20, 10])
    # Plot Classification error vs threshold
    mplot.plot(threshold, classerror, marker="o",label="Misclassification error")
    # Plot Gini index vs threshold
    mplot.plot(threshold, gini, marker="o", label="Gini index")
    # Plot Entropy vs threshold
    mplot.plot(threshold, entropy, marker="o", label="Entropy")
    # Set plot title
    mplot.title("Cost functions Vs Threshold")
    # Set plot x-axis label
    mplot.xlabel("Threshold")
    # Set plot y-axis label
    mplot.ylabel("Cost functions")
    # Set legend
    mplot.legend()

    mplot.show()

def plotmixdata(classerror, gini, entropy, threshold):
    """
           Displays the plot for mixed impurity measures vs threshold

           :param :
            classerror: List of mixed misclassification error
            gini: List of mixed gini indexes
            entropy: List of mixed entropy
            threshold: List of threshold

           :return:
            None
    """
    mplot.figure(figsize=[20, 10])
    # Plot Mixed Classification error vs threshold
    mplot.plot(threshold, classerror, marker="o",label="Mixed Misclassification error")
    # Plot Mixed Gini index vs threshold
    mplot.plot(threshold, gini, marker="o", label="Mixed Gini index")
    # Plot Mixed Entropy vs threshold
    mplot.plot(threshold, entropy, marker="o", label="Mixed Entropy")
    # Set plot title
    mplot.title("Mixed Cost functions Vs Threshold")
    # Set plot x-axis label
    mplot.xlabel("Threshold")
    # Set plot y-axis label
    mplot.ylabel("Mixed Cost functions")
    # Set legend
    mplot.legend()

    mplot.show()

def preprocess(file):
    """
       Preprocess input file data

       :param :
        file: Input csv file

       :return:
        data: preprocessed data

    """
    speedlist = []
    want_to_speed = []

    # open file
    with open(file, encoding="utf-8") as f:
        # Skip first header line
        next(f)
        # read csv data file
        csv_readfile = csv.reader(f, delimiter=',')
        for row in csv_readfile:
            # Pull data for speed
            speedlist.append(row[0])
            # Pull data for want to speed
            want_to_speed.append(row[4])

    return speedlist, want_to_speed

if __name__ == '__main__':
    main()