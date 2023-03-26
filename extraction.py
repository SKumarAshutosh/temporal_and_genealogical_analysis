import requests
import json
import pandas as pd

# Set your Scopus API key
API_KEY = "your_scopus_api_key"


def search_scopus(query, api_key, count=25):
    base_url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept": "application/json",
        "X-ELS-APIKey": api_key
    }
    params = {
        "query": query,
        "count": count
    }
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Error: {response.status_code}")


# Collect biomedical data from Scopus
keywords = ["hypertension", "blood pressure"]
query = " OR ".join([f"TITLE-ABS-KEY({kw})" for kw in keywords])
search_results = search_scopus(query, API_KEY)

# Create an empty DataFrame to store the search results
columns = ["Title", "Authors", "Year", "Publication Name", "Volume", "Issue", "Pages", "DOI", "ISSN", "EID"]
results_df = pd.DataFrame(columns=columns)

# Store the search results in the DataFrame
for item in search_results["search-results"]["entry"]:
    row_data = {
        "Title": item['dc:title'],
        "Authors": ', '.join([author['authname'] for author in item['author']]),
        "Year": item['prism:coverDate'].split('-')[0],
        "Publication Name": item.get('prism:publicationName', 'Not available'),
        "Volume": item.get('prism:volume', 'Not available'),
        "Issue": item.get('prism:issueIdentifier', 'Not available'),
        "Pages": item.get('prism:pageRange', 'Not available'),
        "DOI": item.get('prism:doi', 'Not available'),
        "ISSN": item.get('prism:issn', 'Not available'),
        "EID": item.get('eid', 'Not available')
    }
    results_df = results_df.append(row_data, ignore_index=True)

# Print the DataFrame
print(results_df)

results_df.to_csv("scopus_search_results.csv", index=False)