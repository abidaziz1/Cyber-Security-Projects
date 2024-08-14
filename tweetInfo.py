from re import findall  # Import the findall function from the 're' (regular expression) module to search for patterns in strings
from sys import argv, exit  # Import argv for command-line argument parsing and exit for exiting the script
from urllib.request import urlopen,Request  # Import urlopen from the urllib.request module to open and read URLs
import chardet
import logging

logging.basicConfig(filename='twitter_info.log', level=logging.INFO, format='%(asctime)s %(message)s')
# Function to retrieve information from a given Twitter account
def get(twitter):
    ''' Get information of the given Twitter account link or username '''

    try:
        '''
        Some websites, including Twitter, may block automated requests if they detect them as non-browser requests. To make the script more resilient, you can add a User-Agent header that mimics a real browser.
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
        req = Request(twitter, headers=headers)
        # Open the URL and read the content of the page
        data = urlopen(req).read()
        encoding = chardet.detect(data)['encoding']  # Detect the encoding        # Decode the binary data to a string using utf-8 encoding
        s = data.decode(encoding)
        # Initialize an empty list to store the details
        details = []

        # Extract information like tweets, following, followers, and likes using a regular expression
        [details.append(value) for value in findall('data-is-compact="false">(.*?)<', s)]
        '''
        The script should account for cases where some elements might not be present (e.g., an account has no likes, followers, or tweets). This can be handled by checking the length of the details list or by handling exceptions more gracefully.
        '''
        try:
            # Assign values from the details list to corresponding variables
            following = details[1] if len(details)>1 else 'N/A'
            name      = findall(rb'<title>(.*?) \(', data)[0].decode(encoding)  # Extract the name from the title tag
            tweets    = details[0] if len(details) > 0 else 'N/A'
            followers = details[2] if len(details) >2 else 'N/A'
            likes     = details[3] if len(details) > 3 else 'N/A'
            # Extract the profile picture URL
            pic       = findall(b'href="https://pbs.twimg.com/profile_images(.*?)"', data)[0].decode('utf-8')
            # Extract the account creation date
            date      = findall(b'<span class="ProfileHeaderCard-joinDateText js-tooltip u-dir" dir="ltr" title="(.*?)"', data)[0].decode('utf-8')
        except IndexError:
            print("Error: Could not retrieve some of the information. The page structure may have changed.")
            exit(0)
        # Print the extracted information in a formatted manner
        logging.info('''
        Name: {0}
        Tweets: {1}
        Following: {2}
        Followers: {3}
        Likes: {4}
        Account made in: {5}
        Full profile picture: https://pbs.twimg.com/profile_images{6}
        '''.format(name, tweets, following, followers, likes, date, pic))

    except:
        # Print an error message if something goes wrong (e.g., invalid URL or username)
        print("Error: <twitter_profile_link>/<username> is not correct!")
        exit(0)  # Exit the script

# Prompt the user to enter a Twitter profile link or username
u = input("Enter Twitter profile link or username: ")

# Check if the provided argument is a full Twitter URL; if not, prepend the Twitter URL to the username
if "twitter.com" not in u:
    get("http://x.com/" + u)
else:
    get(u)
