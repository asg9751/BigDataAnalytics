"""
11/03/2018
Author: Amol Gaikwad

Agglomerative Clustering

"""
__author__ = 'Amol Gaikwad'

import sys
import scipy.cluster.hierarchy as scip
import scipy.spatial as scispa
import matplotlib.pyplot as mplot
import warnings
import pandas as pd
import math

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
        # Run agglomeration clusterting
        agglomerate(data)

        # Remove first column
        data = data.iloc[:, 1:]
        print("\n*** Cross correlation coefficients ***\n")
        # Print cross correlation
        corr_data = data.corr()
        with pd.option_context('display.max_rows',None, 'display.max_columns', None):
            print(corr_data)

        # Generate dendogram
        generate_dendogram(data)

def agglomerate(data):
    """
       Run agglomeration clustering on input data

       :param :
        data: input data

       :return:
        None

    """
    # Convert data into key value pair
    data_dict = data.set_index('ID').T.to_dict('list')
    # Dictionary to store cluster indexes
    clusters_dict = {}
    # Dictionary to store last 10 merged smallest clusters
    clusters_merged = {}

    list_cluster_keys = data_dict.keys()
    while(len(list_cluster_keys) > 3):
        # Initialize best distances and keys to infinity
        best_dist_inner = math.inf
        best_dist_outer = math.inf
        best_key_outer = math.inf
        best_key_inner = math.inf

        # Calculate smallest euclidean distance between two rows
        for key_outer, val_outer in data_dict.items():
            for key_inner, val_inner in data_dict.items():
                if (key_outer != key_inner):
                    # Calculate Euclidean distance
                    dist = scispa.distance.euclidean(data_dict[key_outer],data_dict[key_inner])
                    if dist < best_dist_inner:
                        # Record smallest distances and corresponding keys
                        best_dist_inner = dist
                        best_key_inner = key_inner
                        best_key_outer = key_outer

        # If current inner best is less than outer best
        if(best_dist_inner < best_dist_outer):
            best_dist_outer = best_dist_inner
            cluster_val_outer = []
            cluster_val_inner = []
            # Create cluster indexes dictionary
            if best_key_outer in clusters_dict:
                # If larger cluster key already in dictionary
                cluster_val_outer += clusters_dict[best_key_outer]
                if best_key_inner in clusters_dict:
                    # If smaller cluster key already in dictionary append current value to existing ones
                    cluster_val_inner = clusters_dict[best_key_inner]
                    cluster_val_outer += cluster_val_inner
                    cluster_val_outer.append(best_key_inner)
                else:
                    # If smaller cluster key not in dictionary append current smaller value
                    cluster_val_outer.append(best_key_inner)
            else:
                # If larger cluster key not in dictionary
                if best_key_inner in clusters_dict:
                    # If smaller cluster key already in dictionary append current value to existing ones
                    cluster_val_inner = clusters_dict[best_key_inner]
                    cluster_val_outer += cluster_val_inner
                    cluster_val_outer.append(best_key_inner)
                else:
                    # If smaller cluster key not in dictionary append current smaller value
                    cluster_val_outer.append(best_key_inner)


            # Set the cluster indexes in the dictionary
            clusters_dict[best_key_outer] = cluster_val_outer

            # Remove the smaller merged cluster index
            if best_key_inner in clusters_dict:
                clusters_dict.pop(best_key_inner)

            # Store the last 10 merged smaller clusters
            if len(list_cluster_keys) < 14:
                clusters_merged[best_key_inner] = cluster_val_inner

            outer_val = data_dict[best_key_outer]
            inner_val = data_dict[best_key_inner]
            # Calculate average of two rows
            avg_val = get_avg(outer_val, inner_val)
            # Set average value in dictionary
            data_dict[best_key_outer] = avg_val
            # Remove the smaller merged cluster from the data
            data_dict.pop(best_key_inner)

        # Update the cluster keys
        list_cluster_keys = data_dict.keys()

    # Print cluster keys and sizes
    print("*** Cluster Sizes ***")
    for cluster in clusters_dict:
            print("Cluster key "+str(cluster)+" Size "+str(len(clusters_dict[cluster])+1))

    # Print last 10 merged smaller clusters
    print("\n*** Smaller cluster of last 10 merged clusters ***")
    for small_cluster in clusters_merged:
        print("Cluster key " + str(small_cluster) + " Size " + str(len(clusters_merged[small_cluster]) + 1))

def get_avg(out_list, in_list):
    """
       Get average value of two lists

       :param :
        out_list: outer data list
        in_list: inner data list

       :return:
        result_list: list of averaged values

    """
    result_list = []
    for idx in range(0,len(out_list)):
        result_list.append((float(out_list[idx])+float(in_list[idx]))/2)

    return result_list

def generate_dendogram(data):
    """
       Generate dendogram

       :param :
        data: input data

       :return:
        None

    """
    dendgm_data = scip.linkage(data, method='centroid')
    scip.dendrogram(dendgm_data, truncate_mode='lastp', p=30)
    mplot.title("Dendogram plot")
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
    return data


if __name__ == '__main__':
    main()