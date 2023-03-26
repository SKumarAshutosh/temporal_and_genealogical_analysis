import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification

# Load the BioBERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
model = AutoModelForTokenClassification.from_pretrained("cambridgeltl/BioBERT-Ensemble-NER")


# Define a function to apply BioBERT NER
def extract_biomedical_entities_biobert(title):
    inputs = tokenizer(title, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    label_indices = predictions[0].tolist()

    entities = []
    for index, label in enumerate(label_indices):
        if label != 0:  # Ignore the "O" (Outside) label
            entity = tokenizer.decode(inputs["input_ids"][0][index])
            entities.append(entity)

    return entities


# Initialize a list to store the extracted data
data = []

# Iterate through the DataFrame and apply BioBERT NER
for index, row in results_df.iterrows():
    title = preprocess_text(row["Title"])
    entities = extract_biomedical_entities_biobert(title)

    data.append({
        "Title": title,
        "Entities": entities
    })

# Convert the list of dictionaries to a DataFrame
biomedical_entities_biobert_df = pd.DataFrame(data)

# Display the new DataFrame
print(biomedical_entities_biobert_df)
biomedical_entities_biobert_df.to_csv("entities.csv", index=False)