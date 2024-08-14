import requests
import os
import bs4
from urllib.parse import urljoin

# Starting URL of the forum
forum_url = 'http://example.com/forum'
# Create a directory to store the messages
os.makedirs('forum_messages', exist_ok=True)

def download_messages(url):
    print(f'Downloading page {url}...')
    response = requests.get(url)
    response.raise_for_status()
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    # Extract and save messages
    messages = soup.select('.message')  # Update CSS selector as needed
    for i, message in enumerate(messages):
        file_name = os.path.join('forum_messages', f'message_{i}.txt')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(message.get_text(strip=True))
    
    # Find the next page link
    next_link = soup.select_one('a.next')
    if next_link:
        next_url = urljoin(url, next_link['href'])
        download_messages(next_url)

# Start downloading from the first page of the forum
download_messages(forum_url)
print('Done.')
