import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.ikea.com/sa/en/p/franklin-bar-stool-with-backrest-foldable-black-black-60406785/'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

images = soup.find_all('img')

for image in images:

    print(str(image))
    print('***********')
    print('')
    
'''    with open(name.replace(' ', '-').replace('/', '-') + '.jpg', 'wb') as f:
        im = requests.get(link)
        f.write(im.content)'''
