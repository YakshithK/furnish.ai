import pandas as pd
import requests

def is_valid_link(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return not response.url.startswith('https://www.ikea.com/sa/en/cat/products-products/')
    except requests.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False

df = pd.read_csv('ikea-dataset.csv')

df['valid_link'] = df['link'].apply(is_valid_link)
filtered_df = df[df['valid_link']]

df = filtered_df.drop(columns=['valid_link'])

# Save the filtered DataFrame back to a CSV file
filtered_df.to_csv('filtered_furniture.csv', index=False)

print("Filtered CSV file saved successfully.")
