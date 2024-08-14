"""
How It Works
Command Line Arguments: The script takes the recipient's email address and the message body from the command line arguments.

Browser Setup:

The script uses the Chrome WebDriver to automate browser actions. You can switch to another browser by changing the WebDriver initialization.
It navigates to Gmail's login page.
Login Process:

It enters the email address and password into the login fields. These should be securely managed, not hard-coded.
Composing Email:

It clicks the "Compose" button to open the email editor.
It fills in the recipient, subject, and body fields with the provided data.
Sending Email:

It clicks the "Send" button to send the email.
Cleanup:

It waits for the send action to complete, then closes the browser.
"""

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Get email address and message from command line arguments
if len(sys.argv) < 3:
    print('Usage: python emailer.py recipient@example.com "Your message here"')
    sys.exit()

recipient = sys.argv[1]
message = ' '.join(sys.argv[2:])

# Setup the browser and login details
browser = webdriver.Chrome()  # You can use Firefox, Safari, etc.
browser.get('https://mail.google.com/')

# Add your Gmail login credentials here
# Note: It's recommended to use environment variables or a secure method to store credentials
email = 'your_email@gmail.com'
password = 'your_password'

# Find the email input field and enter the email
emailElem = browser.find_element_by_id('identifierId')
emailElem.send_keys(email)
emailElem.send_keys(Keys.ENTER)

# Pause to allow the page to load
time.sleep(2)

# Find the password input field and enter the password
passwordElem = browser.find_element_by_name('password')
passwordElem.send_keys(password)
passwordElem.send_keys(Keys.ENTER)

# Wait for the inbox to load
time.sleep(5)

# Click the "Compose" button
composeElem = browser.find_element_by_class_name('T-I.T-I-KE.L3')
composeElem.click()

# Wait for the compose window to open
time.sleep(2)

# Find the recipient field and enter the recipient's email address
toElem = browser.find_element_by_name('to')
toElem.send_keys(recipient)

# Find the subject field and enter a subject
subjectElem = browser.find_element_by_name('subjectbox')
subjectElem.send_keys('Automated Email')

# Find the body field and enter the message
bodyElem = browser.find_element_by_css_selector('div[aria-label="Message Body"]')
bodyElem.send_keys(message)

# Send the email
sendElem = browser.find_element_by_xpath('//div[@aria-label="Send ‪(Ctrl-Enter)‬"]')
sendElem.click()

# Close the browser
time.sleep(2)
browser.quit()
