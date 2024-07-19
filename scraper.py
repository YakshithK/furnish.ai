import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.ikea.com/sa/en/p/franklin-bar-stool-with-backrest-foldable-black-black-60406785/'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

images = soup.find_all('img')

for image in images:
    if 'srcset' in image.attrs:
        srcset = image.attrs['srcset']
        urls = srcset.split(',')
        
        # Extracting URLs with "xl"
        for url in urls:
            if 'xl' in url:
                # Extracting the URL
                url = url.split()[0]
                print(f"Downloading: {url}")
                img_name = os.path.basename(url.split('?')[0])
                
                # Saving the image
                with open(img_name, 'wb') as f:
                    img_data = requests.get(url).content
                    f.write(img_data)
                print(f"Saved: {img_name}")
                break  # Assuming you want to save only the first "xl" image per img tag
