# IP Look-Up Program
# This program allows users to perform IP address look-up by either entering an IP address, a domain name, or looking up their own IP.
# It provides the following functions:

# Function to collect user input
# - Users choose from various options and provide input based on their choice.
# - It validates the input and returns the IP address or domain name.
# - If the user selects to look up their own IP, it returns a blank query for IP lookup.

import pandas as pd
import requests
import json, re

def collectAddress():
    """
    A Function to collect the user's input IP, Web Domain, or own IP.
    It Validates the input for anomalies and stores the input into a variable, 'Address'. 
    The value is then passed as a parameter to the IP Look-up API
    """
    # Display menu for user choice
    print("******************************************************")
    print("Welcome to IP look-up. Choose from the options below: ")
    print("1. Use an IP address")
    print("2. Use a domain name")
    print("3. Look-up my own IP")
    print("******************************************************")
    choice = input("Your choice is: ")

    if choice == "1":
        # User provides an IP address
        address = input("Enter an IP address: ")
        if address is None:
            print("Enter a valid IP address")
            return None
        else:
            return address
    # RegEx is used to validate the web domain entered by the user
    elif choice == "2":
        # User provides a domain name
        address = input("Enter a domain name: ")
        domain_pattern = r"^(http(s)?://)?([a-zA-Z0-9.-]+\.)+([a-zA-Z]{2,})(/[\w.-/?%&=]*)?$"
        if re.match(domain_pattern, address):
            return address
        else:
            print("Enter a valid domain name")
            return None
    # Returning a blank query param to perform own IP lookup
    elif choice == "3":
        address = ""
        # Alternatively, import get from requests and using this method,
        # address = get('https://api.ipify.org').text can work too
        return address
    else:
        print("An invalid entry. Try again.")
        return None

def ipLookup(query):
    """
    A Function to perform IP address lookup. 
    It Sends a request to a specified IP lookup API.
    Returns IP lookup data in JSON format if the request is successful.
    Handles errors and prints messages if the request fails.
    """
    url = f"http://ip-api.com/json/{query}?fields=26865657"
    params = {
        "query": query,
    }
    r = requests.get(url, json=params)  # Send GET request with JSON data
    if r.status_code == 200:
        data = json.loads(r.text)  # Return JSON response if successful
        print("The IP look-up details are as below:")
        return data
    else:
        print(f"Error: Request failed with status code {r.status_code}")  # Print error message
        return None  # Return None if the request fails

def main():
    """
    The Main function for returning the final output in a data frame.
    Collects user input and performs IP address lookup based on the user's choice.
    Normalizes the response data to flatten nested JSON structures.
    Creates a data frame for further analysis and returns it.
    """
    # Get the query from collectAddress() function
    query = collectAddress()
    # Store the look-up details in a variable
    lookup_details = ipLookup(query)
    # Normalize the response data
    output = pd.json_normalize(lookup_details, record_path=None)
    # Store the data into a data frame for analysis
    df = pd.DataFrame(output)
    df.index = ['Data']
    return df

# Run the main function to execute the program
main()