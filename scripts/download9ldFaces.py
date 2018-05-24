import re
import requests
from bs4 import BeautifulSoup

site = 'http://wiki.9livesdata.com/wiki/index.php/Facebook'
baseURL = 'http://wiki.9livesdata.com'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]

for url in urls:
    filename = url.rsplit('/', 1)[1]
    with open(filename, 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative 
            # if it is provide the base url which also happens 
            # to be the site variable atm. 
            url = baseURL + url
	print(url)
        response = requests.get(url)
        f.write(response.content)
