"""
11/17/2018
Author: Amol Gaikwad

PCA and K-means

"""
__author__ = 'Amol Gaikwad'

import sys
import matplotlib.pyplot as mplot
import warnings
import pandas as pd
import numpy as np
from numpy import linalg as LA
from sklearn.cluster import KMeans

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
        # Remove first column
        data = data.iloc[:, 1:]
        print("\n*** Covariance matrix ***\n")
        # Print covariance
        cov_data = data.cov()
        with pd.option_context('display.max_rows',None, 'display.max_columns', None):
            print(cov_data)

        print("\n********************\n")
        # Get eigen vectors and values
        values, vectors = LA.eig(cov_data)
        print("\n*** Eigen values ***\n")
        # Print eigen values
        print(values)
        print("\n********************\n")
        print("\n*** Eigen vectors ***\n")
        # Print eigen vectors
        print(vectors)
        print("\n********************\n")
        print("\n*** Sorted Eigen values from highest to lowest***\n")
        # Sort eigen values
        values_sorted = sorted(values, reverse=True)
        # Print sorted eigen values
        print(values_sorted)
        print("\n********************\n")

        # Sum sorted eigen values
        sum_eigen = sum(values_sorted)
        # Normalize eigen values
        norm_eigen = values_sorted/sum_eigen

        # Get cumulative sum of normalized eigen values
        cum_sum = np.cumsum(norm_eigen)
        # Insert zero value at start
        cum_sum = np.insert(cum_sum,0,0)

        # Set range for x_data
        x_data = range(0,len(vectors)+1)

        # Plot cum sum Vs number of eigen vectors
        plotdata(x_data,cum_sum, "Cumulative sum Vs Number of eigen vectors","Number of eigen vectors", "Cumulative sum")

        # Get first two eigen vectors with highest eigen values
        eig_pairs = [(np.abs(values[count]), vectors[:, count]) for count in range(len(values))]
        eig_pairs.sort(key=lambda x: x[0], reverse=True)
        count = 0
        eig_list = []
        for pair in eig_pairs:
            if count < 2:
                eig_list.append(pair[1])
                count += 1

        # Project data onto Eigen vector 1
        proj_data_one = data.dot(eig_list[0])
        # Project data onto Eigen vector 2
        proj_data_two = data.dot(eig_list[1])

        print("\n*** First two eigen vectors with largest eigen values ***\n")
        # Print Eigen vector 1
        print(eig_list[0])
        # Print Eigen vector 2
        print(eig_list[1])
        print("\n********************\n")

        # Scatter plot of data onto first two eigen vectors
        plot_scatter_eigen(proj_data_one, proj_data_two)

        # Perform kmeans and return cluster centers
        centers = cluster_kmeans(proj_data_one, proj_data_two)

        # Multiply center of mass and eigen vectors
        proj_data_mass = centers.dot(eig_list)
        print("\n*** First two eigen vectors multiplied by center of mass ***\n")
        # Print multiplied eigen vectors
        print(proj_data_mass)
        print("\n********************\n")

def plot_scatter_eigen(proj_data_one, proj_data_two):
    """
       Show scatter plot of agglomeration data onto first two eigen vectors.

       :param :
        proj_data_one: Data projected on first eigen vector
        proj_data_two: Data projected on second eigen vector

       :return:
        None
    """
    mplot.scatter(proj_data_one, proj_data_two)
    mplot.title("Scatter plot - Original data onto first two eigen vectors")
    mplot.show()

def cluster_kmeans(proj_data_one, proj_data_two):
    """
       Perform Kmeans clustering

       :param :
        proj_data_one: Data projected on first eigen vector
        proj_data_two: Data projected on second eigen vector

       :return:
        centers: cluster centers
    """
    # Perform kmeans for number of clusters = 3
    kmeans = KMeans(n_clusters=3)
    fit_data = np.array(list(zip(proj_data_one, proj_data_two))).reshape(len(proj_data_one), 2)
    kmeans.fit(fit_data)
    # Scatter plot of kmeans data
    mplot.scatter(proj_data_one, proj_data_two, c=kmeans.labels_, cmap='rainbow')
    # Color cluster centers in black
    mplot.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], color='black')
    # Color data points
    colors = ['b', 'g', 'r']
    markers = ['o', 'v', 's']
    for i, l in enumerate(kmeans.labels_):
        mplot.plot(proj_data_one[i], proj_data_two[i], color=colors[l], marker=markers[l], ls='None')

    # Set title
    mplot.title("Kmeans clustering - Cluster center in black")
    # Display scatter plot
    mplot.show()

    # Get cluster centers
    centers = kmeans.cluster_centers_
    print("\n*** Center of mass of clusters ***\n")
    # Print cluster centers
    print(centers)
    print("\n********************\n")

    return centers

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

def preprocess(file):
    """
       Preprocess input file data

       :param :
        file: Input csv file

       :return:
        data: preprocessed data

    """
    data = pd.read_csv(file)
    # Subtract mean from data
    column_mean = data.mean()
    mean = np.matlib.repmat(column_mean, len(data), 1)
    data = data - mean

    return data

if __name__ == '__main__':
    main()