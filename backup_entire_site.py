import requests
import os
import bs4
from urllib.parse import urljoin, urlparse

# Starting URL of the site to back up
start_url = 'http://example.com'
# Create a directory to store the downloaded pages
os.makedirs('backup', exist_ok=True)

# Set to keep track of visited URLs
visited_urls = set()

def download_page(url):
    # Ensure we don't download the same page multiple times
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    print(f'Downloading page {url}...')
    response = requests.get(url)
    response.raise_for_status()
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    # Save the page to the backup directory
    file_name = os.path.join('backup', urlparse(url).path.lstrip('/').replace('/', '_') + '.html')
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    
    # Find all internal links and download them recursively
    for link in soup.find_all('a', href=True):
        full_url = urljoin(url, link['href'])
        # Only follow links within the same domain
        if urlparse(full_url).netloc == urlparse(start_url).netloc:
            download_page(full_url)

# Start downloading from the starting URL
download_page(start_url)
print('Done.')
