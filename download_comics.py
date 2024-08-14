#!/usr/bin/env python3
# downloadXkcd.py - Downloads every single XKCD comic.

import requests
import os
import bs4

# Starting URL
url = 'http://xkcd.com'

# Create a directory to store comics in ./xkcd
os.makedirs('xkcd', exist_ok=True)

while not url.endswith('#'):    # Continues looping until the URL ends with #, which indicates there are no more previous comics.
    # Step 2: Download the Web Page

    print(f'Downloading page {url}...')
    
    # Send a GET request to the current URL
    res = requests.get(url)
    
    # Raise an error if the download failed
    res.raise_for_status()
    
    # Parse the HTML of the downloaded page
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Step 3: Find and Download the Comic Image

    # Find the URL of the comic image
    comicElem = soup.select('#comic img')
    
    # Check if the comic image was found
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl = 'http:' + comicElem[0].get('src')
        
        # Download the image
        print(f'Downloading image {comicUrl}...')
        res = requests.get(comicUrl)
        res.raise_for_status()

        # Step 4: Save the Image and Find the Previous Comic

        # Create a filename for the image
        imageFilePath = os.path.join('xkcd', os.path.basename(comicUrl))
        
        # Open a new file in write-binary mode to save the image
        with open(imageFilePath, 'wb') as imageFile:
            # Write the image data in chunks of 100,000 bytes
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)

    # Find the URL of the Previous Comic button
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print('Done.')
