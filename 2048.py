"""
Browser Initialization:

Start by initializing the browser using Selenium WebDriver. Here, ChromeDriver is used, but you can replace it with any other driver, like GeckoDriver for Firefox.
Open the 2048 Game:

Navigate to the 2048 game's URL.
Wait for the Game to Load:

Use time.sleep() to wait for a couple of seconds, ensuring the game has fully loaded.
Find the HTML Element:

Find the HTML element that listens for keyboard events, typically the <html> tag. This element is used to send keypress events.
Key Sequence:

Define a list of keys representing the sequence of moves. The sequence [Up, Right, Down, Left] is known to be an effective pattern for playing the game.
Automate the Game:

Loop through the defined key sequence, sending each key event to the game. The loop runs for a set duration (end_time) to control how long the script plays the game.
Close the Browser:

After the loop finishes, close the browser to clean up resources.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Initialize the browser (replace 'chromedriver' with the path to your driver)
browser = webdriver.Chrome()

# Open the 2048 game
browser.get('https://gabrielecirulli.github.io/2048/')

# Give the game some time to load
time.sleep(2)

# Get the HTML element that listens for the keypress events
html_elem = browser.find_element_by_tag_name('html')

# Define the sequence of keys to press (Up, Right, Down, Left)
key_sequence = [Keys.UP, Keys.RIGHT, Keys.DOWN, Keys.LEFT]

# Set a duration for how long the script should run
end_time = time.time() + 60  # Run for 60 seconds

# Start playing the game
while time.time() < end_time:
    for key in key_sequence:
        html_elem.send_keys(key)
        time.sleep(0.1)  # Small delay between moves

# Close the browser
browser.quit()