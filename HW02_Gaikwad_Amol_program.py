"""
Author: Amol Gaikwad

This program builds a one dimensional classifier from vehicle data set. It plots the cost function vs threshold speed.
Finally, it plots the ROC curve showing a plot of true positive rate vs false positive rate.

"""
__author__ = 'Amol Gaikwad'

import sys
import csv
import math
import numpy as np
import warnings
import matplotlib.pyplot as mplot

def main():
    """
        Main Program
        Handle command line arguments. Perform one dimensional classification and display plots.

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

        # Round the speed data
        speedlist = [round(float(i)) for i in speedlist]

        # Perform one dimensional classification and return
        threshold_list, cost_function_list, false_alarm_rate_list, true_positive_rate_list, lowest_cost_fp, lowest_cost_tp = one_dimensional(speedlist, want_to_speed)

        # Compute Otsu's threshold
        otsu_threshold = otsu(speedlist)

        # Print Otsu's threshold
        print("Otsu threshold is "+str(otsu_threshold)+" mph")

        # Print point on ROC curve corresponding to lowest value of cost function
        print("Point with lowest cost function on ROC curve ("+str(lowest_cost_fp)+", "+str(lowest_cost_tp)+")")

        # Plot cost function vs threshold speed
        plotdata(threshold_list,cost_function_list,"Cost function vs Threshold", "Threshold speed in mph", "Cost function")

        # Plot ROC curve
        roc_curve_plot(false_alarm_rate_list, true_positive_rate_list,"ROC curve", "False positive rate", "True positive rate", lowest_cost_fp, lowest_cost_tp)

def one_dimensional(data, want_to_speed):
    """
           Implement one dimensional classification. Compute best threshold to minimize cost function, false negatives,
           false positives, true positives and true negatives and returns data for plots.

           :param :
            data: Input speed data for classification
            want_to_speed: Input data values for drivers wanting to speed

           :return:
            threshold_list: Returns list of speed threshold values
            cost_function_list: Returns list of cost function values
            false_alarm_rate_list: Returns list of false positive rate values
            true_positive_rate_list: Returns list of true positive rate values
            lowest_cost_fp: Returns false positive rate value for lowest cost function
            lowest_cost_tp: Returns true positive rate value for lowest cost function

    """

    # set the best misclassification rate and best threshold to infinity
    best_misclass_rate = math.inf
    best_threshold = math.inf

    # set the false positive rate value and true positive rate value for lowest cost function to 0
    lowest_cost_fp = 0
    lowest_cost_tp = 0

    # set the range of threshold values
    threshold_min = math.floor(min(data))
    threshold_max = math.ceil(max(data))

    # list to store cost function values
    cost_function_list =[]
    # list to store threshold values
    threshold_list =[]
    # list to store false positives rate
    false_alarm_rate_list = []
    # list to store true positives rate
    true_positive_rate_list = []
    # set number of aggressive drivers let through to 0
    num_aggressive_drivers = 0
    # set the non reckless drivers pulled over to 0
    num_nonreckless_drivers = 0

    for threshold in range(threshold_min, threshold_max):
        # initialize cost function to 0
        cost_function = 0
        # list to store misses or false negatives
        list_misses = []
        # list to store false positives
        list_false_alarm = []
        # list to store true positives
        list_true_positive = []
        # add threshold value to threshold list
        threshold_list.append(threshold)
        # Initialize count of drivers having want to speed as 0 to 0
        num_not_speeding = 0
        # Initialize count of drivers having want to speed as 1 to 0
        num_speeding = 0


        for index in range(0, len(data)):
            if data[index] < threshold:
                # Drivers having speed less than threshold
                if int(want_to_speed[index]) == 1:
                    # Drivers having having speed less than threshold and want to speed as 1. Add to list of misses.
                    list_misses.append(data[index])
                    # Increment count of drivers having want to speed as 1
                    num_speeding += 1
                else:
                    # Increment count of drivers having want to speed as 0
                    num_not_speeding += 1
            elif data[index] >= threshold:
                # Drivers having speed more than equal to threshold
                if int(want_to_speed[index]) == 0:
                    # Add to list of false alarms i.e. false positives.
                    list_false_alarm.append(data[index])
                    # Increment count of drivers having want to speed as 0
                    num_not_speeding+= 1
                else:
                    # Add to list of true positives.
                    list_true_positive.append(data[index])
                    # Increment count of drivers having want to speed as 1
                    num_speeding += 1

        # Define cost function
        cost_function = len(list_misses) + 3 * len(list_false_alarm)
        # Add computed cost function to list
        cost_function_list.append(cost_function)


        if cost_function <= best_misclass_rate:
            # Set best_misclass_rate and best_threshold
            best_misclass_rate = cost_function
            best_threshold = threshold
            # Count aggressive drivers let through
            num_aggressive_drivers = len(list_misses)
            # Count non reckless drivers pulled over
            num_nonreckless_drivers = len(list_false_alarm)
            # Computes false positive rate value for lowest cost function
            lowest_cost_fp = len(list_false_alarm)/ num_not_speeding
            # Computes true positive rate value for lowest cost function
            lowest_cost_tp = len(list_true_positive)/ num_speeding

        # Compute false alarm rate
        false_alarm_rate_list.append(len(list_false_alarm)/ num_not_speeding)
        # Compute true positive rate
        true_positive_rate_list.append(len(list_true_positive)/ num_speeding)

    # Print one dimensional threshold
    print("One dimensional classifier threshold " + str(best_threshold)+" mph")
    # Print number of aggressive drivers let through i.e. false negatives
    print("No of aggressive drivers let through is "+str(num_aggressive_drivers))
    # Print number of non reckless drivers pulled over i.e. false positives
    print("No of non reckless drivers pulled over is " + str(num_nonreckless_drivers))

    return threshold_list, cost_function_list, false_alarm_rate_list, true_positive_rate_list, lowest_cost_fp, lowest_cost_tp

def otsu(data):
    """
       Implement Otsu's method to separate data into clusters

       :param :
        data: Input data from which clusters are to be formed

       :return:
        best_threshold: Returns the best threshold value using which clusters can be split

    """
    # set the best mix varaiance and best threshold to infinity
    best_mix_variance = math.inf
    best_threshold = math.inf

    for threshold in data:
        # Get data points less than equal to threshold
        wt_under = [float(point) for point in data if float(point) <= float(threshold)]
        # Get data points greater than threshold
        wt_over = [float(point) for point in data if float(point) > float(threshold)]
        # calculate weight under fraction
        wt_under_fraction = len(wt_under) / len(data)
        # calculate weight over fraction
        wt_over_fraction = len(wt_over) / len(data)

        # calculate variance under
        variance_under = np.var(wt_under)
        # calculate variance over
        variance_over = np.var(wt_over)
        # calculate mix variance
        mix_variance = wt_under_fraction * variance_under + wt_over_fraction * variance_over

        # Set best mix variance and best threshold
        if mix_variance < best_mix_variance:
            best_mix_variance = mix_variance
            best_threshold = threshold

    return best_threshold

def plotdata(xdata, ydata, title, xlabel, ylabel):
    """
       Displays the plot for ydata vs xdata

       :param :
        xdata: Input data to be plotted on x axis
        ydata: Input data to be plotted on y axis
        title: Title of plot
        xlabel: Label x axis
        ylabel: Label y axis

       :return:
        None
    """
    mplot.figure(figsize=[20, 10])
    # Plot input data vs random data
    mplot.plot(xdata, ydata, marker="o")
    # Set plot title
    mplot.title(title)
    # Set plot x-axis label
    mplot.xlabel(xlabel)
    # Set plot y-axis label
    mplot.ylabel(ylabel)

    mplot.show()

def roc_curve_plot(xdata, ydata, title, xlabel, ylabel, xpoint, ypoint):
    """
       Displays the ROC curve plot for ydata vs xdata

       :param :
        xdata: Input data to be plotted on x axis
        ydata: Input data to be plotted on y axis
        title: Title of plot
        xlabel: Label x axis
        ylabel: Label y axis
        xpoint: x value of point to be highlighted
        ypoint: y value of point to be highlighted

       :return:
        None
    """
    mplot.figure(figsize=[20, 10])
    # Plot input data vs random data
    mplot.plot(xdata, ydata, marker="o")
    # Set plot title
    mplot.title(title)
    # Set plot x-axis label
    mplot.xlabel(xlabel)
    # Set plot y-axis label
    mplot.ylabel(ylabel)
    # Draw a circle around a particular point to highlight it
    circle1 = mplot.Circle((xpoint, ypoint), 0.02, color='r', fill=False)
    mplot.gcf().gca().add_artist(circle1)

    # Write text at given location on graph
    mplot.text(xpoint+0.03,ypoint,"Point with lowest cost function ("+str(round(xpoint,2))+", "+str(round(ypoint,2))+")")

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