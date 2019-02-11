"""
Author: Amol Gaikwad

This program implements clustering using Otsu's method. It plots the input data against random noise. Then it performs
Parzen density estimation.

"""
__author__ = 'Amol Gaikwad'

import sys
import csv
import math
import numpy as np
import warnings
import random
import matplotlib.pyplot as mplot

def main():
    """
        Main Program
        Handle command line arguments

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

        # Preprocess the input file to remove durations less than 0.5 seconds
        data = preprocess(file)
        # Print the total data points after cleaning
        print("Total number of data points "+str(len(data))+"\n")

        # Calculate otsu's threshold for cluster1
        otsu_threshold = otsu(data)
        # Make clusters based on otsu's threshold
        clusterbig1, clustersmall1 = make_cluster(data, otsu_threshold)

        # Calculate otsu's threshold for cluster2
        otsu_threshold2 = otsu(clusterbig1)
        # Make clusters based on otsu's threshold
        clusterbig2, clustersmall2 = make_cluster(clusterbig1, otsu_threshold2)

        # Calculate otsu's threshold for cluster3
        otsu_threshold3 = otsu(clusterbig2)
        # Make clusters based on otsu's threshold
        clusterbig3, clustersmall3 = make_cluster(clusterbig2, otsu_threshold3)

        # Display cluster properties sorted by average duration
        show_cluster_features(clusterbig3, 0.5)
        show_cluster_features(clustersmall3, otsu_threshold3)
        show_cluster_features(clustersmall2, otsu_threshold2)
        show_cluster_features(clustersmall1, otsu_threshold)

        # Plot input data against random noise
        plotdata(data)

        # Plot parzen density estimate
        parzenestimate(data)

def parzenestimate(data):
    """
       Displays the parzen density estimate

       :param :
        data: Input data to be plotted

       :return:
        None
    """
    # Dictionary to store frequency count of data points
    freq_count={}
    # list of x-data points
    x_data = []
    # list of y-data points
    y_data = []
    # add data point to dictionary
    for point in data:
        # take ceil of data point
        ceilpoint = math.ceil(float(point))
        # increase frequency count by 1
        freq_count[ceilpoint] = freq_count.get(ceilpoint,0)+1

    # sort dictionary items
    sorted_freq_count = sorted(freq_count.items())
    # populate x and y data points
    for key, val in sorted_freq_count:
        x_data.append(key)
        y_data.append(val)

    # Plot duration in seconds vs frequency count
    mplot.plot(x_data, y_data)
    # Set plot title
    mplot.title("Parzen density estimation")
    # Set plot x-axis label
    mplot.xlabel("Stop duration in secs")
    # Set plot y-axis label
    mplot.ylabel("Counts per duration")

    mplot.show()

def plotdata(data):
    """
       Displays the plot for input data vs random noise

       :param :
        data: Input data to be plotted

       :return:
        None
    """
    # Get input data in float format
    numdata = [float(point) for point in data]
    # Get random data
    x = [random.uniform(0, 1) for count in range(0, len(numdata))]

    mplot.figure(figsize=[20, 10])
    # Plot input data vs random data
    mplot.plot(numdata, x, 'o')
    # Set plot title
    mplot.title("Stop duration in seconds VS Random noise")
    # Set plot x-axis label
    mplot.xlabel("Stop duration in secs")
    # Set plot y-axis label
    mplot.ylabel("Random noise")

    mplot.show()


def make_cluster(data, threshold):
    """
       Makes two clusters from input data. One having all data points above threshold and other having all data
       points less than equal to threshold

       :param :
        data: Input data containing stopped durations
        threshold: Threshold value used for making clusters

       :return:
        biggercluster: Cluster with bigger size
        smallercluster: Cluster with smaller size
    """
    # Make cluster of data points less than equal to threshold
    cluster_lower = [point for point in data if float(point) <= float(threshold)]
    # Make cluster of data points greater than threshold
    cluster_upper = [point for point in data if float(point) > float(threshold)]

    # Find out bigger and smaller clusters
    if len(cluster_lower) >= len(cluster_upper):
        biggercluster = cluster_lower
        smallercluster = cluster_upper
    else:
        biggercluster = cluster_upper
        smallercluster = cluster_lower

    # Return bigger and smaller clusters
    return biggercluster, smallercluster

def show_cluster_features(cluster, threshold):
    """
        Displays all properties of a cluster

       :param :
        cluster: Cluster whose properties are to be displayed
        threshold: Threshold value used for the cluster

       :return:
        None
    """
    # calculate size of cluster
    size = len(cluster)
    # calculate sum of points in cluster
    total = sum([float(point) for point in cluster])
    # calculate average of points
    avg = total / size
    # Print cluster properties
    print("***** Cluster *******")
    print("Cluster size "+ str(size))
    print("Average duration value "+ str(avg))
    print("Standard deviation is " + str(np.std([float(point) for point in cluster])))
    print("Minimum duration value " + str(min([float(point) for point in cluster])))
    print("Maximum duration value " + str(max([float(point) for point in cluster])))
    print("Threshold duration value " + str(threshold))
    print("***** End of cluster *******\n")


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

def preprocess(file):
    """
       Preprocess input file data and remove

       :param :
        file: Input csv file

       :return:
        data: preprocessed data

    """
    data = []
    # open file
    with open(file, encoding="utf-8") as f:
        # Skip first header line
        next(f)
        # read csv data file
        csv_readfile = csv.reader(f, delimiter=',')
        for row in csv_readfile:
            # Filter data and remove durations less than 0.5 seconds
            if float(row[1]) >= 0.5:
                data.append(row[1])

    return data

if __name__ == '__main__':
    main()