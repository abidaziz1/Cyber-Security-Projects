import requests
import os
import bs4
from urllib.parse import urljoin

# Starting URL of the online store's catalog
catalog_url = 'http://example.com/store/catalog'
# Create a directory to store the catalog items
os.makedirs('store_catalog', exist_ok=True)

def download_catalog(url):
    print(f'Downloading page {url}...')
    response = requests.get(url)
    response.raise_for_status()
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    # Extract and save item details
    items = soup.select('.item')  # Update CSS selector as needed
    for i, item in enumerate(items):
        item_name = item.select_one('.item-name').get_text(strip=True)
        item_price = item.select_one('.item-price').get_text(strip=True)
        item_description = item.select_one('.item-description').get_text(strip=True)
        
        file_name = os.path.join('store_catalog', f'item_{i}.txt')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f'Name: {item_name}\n')
            file.write(f'Price: {item_price}\n')
            file.write(f'Description: {item_description}\n')
    
    # Find the next page link
    next_link = soup.select_one('a.next')
    if next_link:
        next_url = urljoin(url, next_link['href'])
        download_catalog(next_url)

# Start downloading from the first page of the catalog
download_catalog(catalog_url)
print('Done.')
