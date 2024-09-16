
import requests
import sys
import threading

# Function to check if subdomain is valid
def check_subdomain(subdomain):
    try:
        # Check both http and https versions
        for protocol in ['http', 'https']:
            url = f"{protocol}://{subdomain}"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            if response.status_code == 200:
                print(f"Valid domain: {url}")
            else:
                print(f"Potentially reachable, but non-200 response: {url}")
    except requests.ConnectionError:
        # Ignore failed connections
        pass
    except requests.Timeout:
        # Ignore timeouts, print a message if needed
        print(f"Timeout for {subdomain}")
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Error checking {subdomain}: {str(e)}")

# Main part of the code
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python subdomain_enum.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    sub_list = open("subdomains.txt").read()
    subdoms = sub_list.splitlines()

    threads = []

    # Using threading to check subdomains in parallel
    for sub in subdoms:
        sub_domain = f"{sub}.{domain}"
        t = threading.Thread(target=check_subdomain, args=(sub_domain,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()
"""
Threading:

We create a thread for each subdomain to check them in parallel. This speeds up the process significantly, especially when dealing with large subdomain lists.
HTTP and HTTPS Check:

We check both http:// and https:// versions of each subdomain since some domains might default to HTTPS or redirect to it.
User-Agent Header:

A User-Agent header mimicking a real browser (Mozilla/5.0) is added to avoid being blocked by some servers.
Timeout Handling:

A timeout of 5 seconds is set for each request to avoid hanging on slow or non-responsive subdomains.
Improved Error Handling:

Errors like timeouts or connection failures are handled gracefully. If an unexpected error occurs, it is caught and printed.
"""
