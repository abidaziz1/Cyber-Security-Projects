"""
Use Case:
Automatically open all review pages for a specific product to read user reviews from multiple sources.

Algorithm:
Get Product URL: Read the URL of the product page.
Send Request to Review Sites: Send requests to multiple review sites.
Parse Review Results: Parse the review results pages.
Extract Review Links: Extract the links to the reviews.
Open Review Links in Tabs: Open each review link in a new browser tab.
"""
import requests
import sys
import webbrowser
import bs4
import time

# Get search keywords from user
search_keywords = input("Enter search keywords: ")

# List of review sites with product URL search feature
review_sites = [
    f'https://www.amazon.com/s?k={search_keywords}',
    f'https://www.goodreads.com/search?q={search_keywords}',
    f'https://www.bookshop.org/search?q={search_keywords}'
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

for review_site in review_sites:
    response = requests.get(review_site, headers=headers)
    response.raise_for_status()
    time.sleep(1)  # wait for 1 second before making the next request

    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    link_elements = soup.find_all('a', href=True)  # Find all anchor tags with an href attribute

    num_links_to_open = min(5, len(link_elements))
    for i in range(num_links_to_open):
        link = link_elements[i]['href']
        if not link.startswith('http'):  # Check if the link is relative
            link = review_site + link
        webbrowser.open(link)