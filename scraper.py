import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def split_string(input_string):
    first_dash_pos = input_string.find('-')
    second_part_start = input_string.find('-', first_dash_pos + 1)

    category = input_string[:second_part_start]
    name = input_string[second_part_start:].strip('-').split(',')[0]

def is_valid_link(url):
    try:
        response = requests.get(url, allow_redirects=True)
        return not response.url.startswith('https://www.ikea.com/sa/en/cat/products-products/')
    except requests.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False

df = pd.read_csv('ikea-dataset.csv')

df['valid_link'] = df['link'].apply(is_valid_link)
df = df[df['valid_link']]

print(df.head())
print('-'*50)

image_directory = 'database/images'

# Create the directory if it doesn't exist
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# Iterate through each row in the dataframe
for row in df.iterrows():
    data = row[1]
    name = data['category']
    item_desc = data['short_description']
    name_id = f"{name}-{item_desc}"
    name_id = name_id.replace(' ', '-').replace('/', '').replace(',', '')

    url = data['link']

    # Make the request
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find all image tags
    images = soup.find_all('img')

    # Flag to stop after the first valid image
    found_image = False

    # Iterate over all images
    for image in images:
        if 'srcset' in image.attrs:
            srcset = image.attrs['srcset']
            urls = srcset.split(',')

            # Extract URLs with "xl"
            for url in urls:
                if 'xl' in url:
                    # Extract the URL
                    url = url.split()[0]
                    print(f"Downloading: {url}")

                    # Extract the file extension from the URL
                    file_extension = os.path.splitext(url.split('?')[0])[1]
                    img_name = f"{name_id}{file_extension}"
                    img_path = os.path.join(image_directory, img_name)

                    # Save the image
                    with open(img_path, 'wb') as f:
                        img_data = requests.get(url).content
                        f.write(img_data)
                    print(f"Saved: {img_path}")

                    # Set the flag to True and break out of the loop
                    found_image = True
                    break
            if found_image:
                break