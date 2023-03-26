import networkx as nx
import pandas as pd
import numpy as np

# load the data frame with nodes and edges and timestamps
df = pd.read_csv('knowledge_graph.csv')

# convert the data frame to a networkx graph object
graph = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr=True)

# initialize empty dictionaries to store the graph metrics over time
degree_centrality = {}
betweenness_centrality = {}
clustering_coefficient = {}

# loop through each timestamp and calculate graph metrics
for timestamp in df['timestamp'].unique():
    # extract subgraph for the given timestamp
    subgraph = graph.subgraph(df.loc[df['timestamp'] == timestamp, 'source':'target'])

    # calculate degree centrality
    degree_centrality[timestamp] = nx.degree_centrality(subgraph)

    # calculate betweenness centrality
    betweenness_centrality[timestamp] = nx.betweenness_centrality(subgraph)

    # calculate clustering coefficient
    clustering_coefficient[timestamp] = nx.clustering(subgraph)

# convert the dictionaries to data frames
degree_centrality_df = pd.DataFrame(degree_centrality)
betweenness_centrality_df = pd.DataFrame(betweenness_centrality)
clustering_coefficient_df = pd.DataFrame(clustering_coefficient)

# compute mean and standard deviation for each metric across all timestamps
mean_degree_centrality = degree_centrality_df.mean(axis=1)
std_degree_centrality = degree_centrality_df.std(axis=1)

mean_betweenness_centrality = betweenness_centrality_df.mean(axis=1)
std_betweenness_centrality = betweenness_centrality_df.std(axis=1)

mean_clustering_coefficient = clustering_coefficient_df.mean(axis=1)
std_clustering_coefficient = clustering_coefficient_df.std(axis=1)

# save the mean and standard deviation to a data frame
metrics_df = pd.DataFrame({'mean_degree_centrality': mean_degree_centrality,
                           'std_degree_centrality': std_degree_centrality,
                           'mean_betweenness_centrality': mean_betweenness_centrality,
                           'std_betweenness_centrality': std_betweenness_centrality,
                           'mean_clustering_coefficient': mean_clustering_coefficient,
                           'std_clustering_coefficient': std_clustering_coefficient})

# save the data frame to a CSV file
metrics_df.to_csv('graph_metrics.csv', index_label='timestamp')