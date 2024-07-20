import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# URL to scrape
url = 'https://www.ikea.com/sa/en/p/ekedalen-bar-table-dark-brown-90400517/'

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
                img_name = os.path.basename(url.split('?')[0])

                # Save the image
                with open(img_name, 'wb') as f:
                    img_data = requests.get(url).content
                    f.write(img_data)
                print(f"Saved: {img_name}")

                # Set the flag to True and break out of the loop
                found_image = True
                break
        if found_image:
            break
