# This code opens Firefox and navigates to the specified URL.
from selenium import webdriver
browser = webdriver.Firefox()
browser.get('http://inventwithpython.com')
# The tag_name attribute can be used to identify the tag of the found element.
elem = browser.find_element_by_class_name('bookcover')
# Web elements can be clicked using the click() method
linkElem = browser.find_element_by_link_text('Read It Online')
linkElem.click()


# Working with Forms
# Use send_keys() to input text into form fields
browser = webdriver.Firefox()
browser.get('http://gmail.com')
emailElem = browser.find_element_by_id('Email')
emailElem.send_keys('not_my_real_email@gmail.com')
passwordElem = browser.find_element_by_id('Passwd')
passwordElem.send_keys('12345')
# Submit forms using the submit() method
passwordElem.submit()
'''As long as Gmail hasn’t changed the id of the Username and Pass
word text fields since this book was published, the previous code will fill in 
those text fields with the provided text.'''


# Sending Special Keys(keyboard)
from selenium.webdriver.common.keys import Keys
htmlElem.send_keys(Keys.END)  # Scroll to bottom
htmlElem.send_keys(Keys.HOME)  # Scroll to top

'''Keys.DOWN, Keys.UP, Keys.LEFT,  
Keys.RIGHT               The keyboard arrow keys
 Keys.ENTER, Keys.RETURN
 Keys.HOME, Keys.END, Keys.PAGE_DOWN, 
Keys.PAGE_UP         The home, end, pagedown, and pageup keys
 Keys.ESCAPE, Keys.BACK_SPACE,  
Keys.DELETE      The esc, backspace, and delete keys
 Keys.F1, Keys.F2,  .  .  . , Keys.F12       The F1 to F12 keys at the top of the keyboard
 Keys.TAB       The tab key
'''


# Browser Navigation
#Browser Buttons
browser.back()  # Click Back button
browser.forward()  # Click Forward button
browser.refresh()  # Click Refresh button
browser.quit()  # Close the browser
