import networkx as nx
import pandas as pd

# Compute graph metrics
degree_centrality = nx.degree_centrality(graph)
betweenness_centrality = nx.betweenness_centrality(graph)
clustering_coefficient = nx.clustering(graph)

# Organize time-stamped data into a time series format
time_series = pd.DataFrame.from_dict(timestamps, orient='index', columns=['timestamp'])

# Compute temporal patterns
time_series['year'] = pd.to_datetime(time_series['timestamp']).dt.year
time_series['month'] = pd.to_datetime(time_series['timestamp']).dt.month
time_series['quarter'] = pd.to_datetime(time_series['timestamp']).dt.quarter
time_series['day_of_week'] = pd.to_datetime(time_series['timestamp']).dt.dayofweek

# Extract feature values for each entity and relationship
features = []
for node in graph.nodes():
    feature = {'id': node, 'degree_centrality': degree_centrality[node],
               'betweenness_centrality': betweenness_centrality[node],
               'clustering_coefficient': clustering_coefficient[node]}
    entity_ts = time_series.loc[time_series.index == node]
    feature.update(entity_ts[['year', 'month', 'quarter', 'day_of_week']].iloc[0].to_dict())
    features.append(feature)

features_df = pd.DataFrame(features)