import pandas as pd

# Assuming nodes_df and relations_df are the DataFrames generated in the previous step
nodes_df["original_source"] = ""

# Loop through each row in the relations_df DataFrame
for _, row in relations_df.iterrows():
    title = row["Title"]
    timestamp = row["timestamp"]
    entities = row["Entities"]

    for entity in entities:
        # Check if the current entity exists in the nodes_df DataFrame
        entity_mask = nodes_df["id"] == entity

        if nodes_df.loc[entity_mask, "original_source"].empty:
            # If the entity does not have an original source, assign the current title as its source
            nodes_df.loc[entity_mask, "original_source"] = title
        else:
            # If the entity already has an original source, update the source only if the current timestamp is earlier
            existing_timestamp = nodes_df.loc[entity_mask, "timestamp"].iloc[0]
            if timestamp < existing_timestamp:
                nodes_df.loc[entity_mask, "original_source"] = title
                nodes_df.loc[entity_mask, "timestamp"] = timestamp

# Display the updated nodes_df DataFrame
print(nodes_df)