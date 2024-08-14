"""
Setup:

Search Keyword & Directory: Specify the keyword to search for and create a directory to store downloaded images.
Browser Initialization: Launch the browser using Selenium.
Search for Images:

Search Box Interaction: Locate the search box element and enter the search keyword. Then, press the return key to initiate the search.
Scrolling: Scroll down the page to load more images if necessary. The loop controls how many times to scroll, and the sleep interval ensures the page has time to load.
Download Images:

Find Image Elements: Locate image elements on the page.
Download Function: Define a function to download images from their URLs.
Loop & Download: Loop through the image elements, extract the URLs, and download them using the defined function.
Cleanup:

Close the Browser: Once all images are downloaded, close the browser.
"""

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the search keyword and the number of images to download
search_keyword = 'nature'
download_dir = 'downloaded_images'

# Create a directory for downloaded images if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Set up the browser (replace 'chromedriver' with your driver)
browser = webdriver.Chrome()  # or `webdriver.Firefox()`
browser.get('https://imgur.com/')

# Find the search box and enter the search keyword
search_box = browser.find_element_by_xpath('//input[@placeholder="Search"]')
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)

# Allow some time for the results to load
time.sleep(5)

# Scroll down to load more images if necessary
for _ in range(5):  # adjust range for more scrolling
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Find image elements and extract URLs
image_elements = browser.find_elements_by_xpath('//img[@src]')

# Define a function to download an image
def download_image(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(dest_folder, url.split('/')[-1])
        with open(file_path, 'wb') as file:
            file.write(response.content)

# Loop through image elements and download each image
for img_elem in image_elements:
    img_url = img_elem.get_attribute('src')
    # Filter only valid image URLs
    if img_url.startswith('http') and 'i.imgur.com' in img_url:
        download_image(img_url, download_dir)

# Close the browser
browser.quit()