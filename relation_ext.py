import torch
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('dmis-lab/biobert-base-cased-v1.1')


def extract_relations_biobert(title, entities):
    relations = []

    if not entities:
        return relations

    encoded_title = model.encode(title, convert_to_tensor=True)

    for entity1 in entities:
        for entity2 in entities:
            if entity1 != entity2:
                combined_sentence = f"{entity1} - {entity2}"
                encoded_combined_sentence = model.encode(combined_sentence, convert_to_tensor=True)

                similarity = util.pytorch_cos_sim(encoded_title, encoded_combined_sentence)

                if similarity > 0.5:  # You can adjust this threshold based on your dataset and requirements
                    relations.append((entity1, entity2))

    return relations


data = []

for index, row in biomedical_entities_biobert_df.iterrows():
    title = row["Title"]
    entities = row["Entities"]
    relations = extract_relations_biobert(title, entities)

    data.append({
        "Title": title,
        "Entities": entities,
        "Relations": relations
    })

# Convert the list of dictionaries to a DataFrame
relations_df = pd.DataFrame(data)

# Display the new DataFrame
print(relations_df)