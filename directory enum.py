"""
Key Concepts:
200 OK: Indicates that the directory or file exists.
403 Forbidden: Means the directory exists but is not accessible (could be sensitive).
404 Not Found: Indicates that the directory or file doesn't exist.
301/302 Redirect: Indicates a directory might exist, but the server is redirecting requests (could point to an important resource).
"""
import requests
import sys
import threading

# Function to check each directory
def check_directory(directory):
    try:
        # Try both .html and no extension
        for extension in ['', '.html', '.php', '.js', '.asp', '.txt', '.bak']:
            url = f"http://{sys.argv[1]}/{directory}{extension}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            
            if r.status_code == 200:
                print(f"Valid directory: {url}")
            elif r.status_code == 403:
                print(f"Forbidden directory (403): {url}")
            elif r.status_code == 301 or r.status_code == 302:
                print(f"Redirect found (potential valid directory): {url}")
    except requests.ConnectionError:
        pass
    except requests.Timeout:
        print(f"Timeout for {directory}")
    except Exception as e:
        print(f"Error checking {directory}: {str(e)}")

# Main script logic
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python directory_enum.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    # Read wordlist file for directories
    wordlist = open("wordlist.txt").read()
    directories = wordlist.splitlines()

    # Use threading to check directories concurrently
    threads = []
    
    for directory in directories:
        t = threading.Thread(target=check_directory, args=(directory,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()
"""
Threading for Speed:

Similar to subdomain enumeration, threading is introduced to check directories in parallel, speeding up the process significantly, especially when dealing with large wordlists.
Check for Multiple Extensions:

Some directories might have .html, .php, .asp, or no extension. This version checks directories both with and without an extension (in this case, .html). You can extend it further to check for other common file extensions like .php, .jsp, etc.
Error Handling:

Added error handling for connection timeouts and connection errors to make sure the script doesn't fail and can handle slow or unresponsive servers.
Response Code Checks:

403 Forbidden: This status code can be important because it indicates that the directory exists but the server is restricting access.
301/302 Redirect: These response codes suggest that the server is redirecting requests. This could indicate the presence of a directory that redirects traffic elsewhere, which might be a valid resource.
User-Agent Header:

Added a User-Agent to mimic a browser to avoid being blocked by some websites that may filter requests based on headers.
Timeouts:

Added a 5-second timeout for each request to avoid hanging on unresponsive directories. You can adjust the timeout depending on your needs.
"""
