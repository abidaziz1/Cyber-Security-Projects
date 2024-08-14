"""
Automatically open links to photos after performing a search on a photo site like Flickr or Imgur.

Algorithm:
Get Search Keywords from Command Line: Read the photo search keywords.
Send Search Request: Send an HTTP request to the photo site's search URL.
Parse Search Results: Use BeautifulSoup to parse the search results page.
Extract Photo Links: Use CSS selectors to extract the photo links.
Open Photo Links in Tabs: Open each photo link in a new browser tab.
"""

import requests
import sys
import webbrowser
import bs4

print('Searching Flickr...')

# Get search keywords from command line arguments
search_keywords = ' '.join(sys.argv[1:])
search_url = f'https://www.flickr.com/search/?text={search_keywords}'

response = requests.get(search_url)
response.raise_for_status()

soup = bs4.BeautifulSoup(response.text, 'html.parser')
link_elements = soup.select('.photo-list-photo-view a')  # Update CSS selector as needed

num_links_to_open = min(5, len(link_elements))
for i in range(num_links_to_open):
    link = 'https://www.flickr.com' + link_elements[i].get('href')
    webbrowser.open(link)
