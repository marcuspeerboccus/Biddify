import requests

# Replace with your credentials and token
LOGIN_URL = "https://autohelperbot.com/login"  # Replace with the actual login URL
PAYLOAD = {
    "email": "marcusturbo@yahoo.com",
    "password": "newpass",
    "undefined": "Next"  # This might be a hidden field or button value
}

# Create a session to persist cookies
session = requests.Session()

# Add headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}
session.headers.update(headers)

# Step 1: First get the login page to get any necessary tokens and cookies
try:
    response = session.get(LOGIN_URL)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Extract the CSRF token from the page
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    token_element = soup.find("input", {"name": "_token"})
    if token_element:
        PAYLOAD["_token"] = token_element["value"]
    
    # Step 2: Send a POST request to log in
    login_response = session.post(LOGIN_URL, data=PAYLOAD)
    login_response.raise_for_status()
    
    # Step 3: Check if login was successful (adjust conditions based on the site's behavior)
    if login_response.status_code == 200:
        if "Welcome" in login_response.text or "Dashboard" in login_response.text:
            print("Login successful!")
            
            # Step 4: Use the session to access authenticated pages
            SALES_URL = "https://autohelperbot.com/sales?vehicle=AUTOMOBILE&year_from=2020&year_to=2024&make_id=8773&model_id=52810&_=1739238328991&page=1"
            sales_response = session.get(SALES_URL)
            sales_response.raise_for_status()
            
            # Step 5: Parse the sales data
            if sales_response.status_code == 200:
                print("Sales data retrieved successfully!")
                print(sales_response.text)  # Replace with your parsing logic
            else:
                print(f"Failed to retrieve sales data. Status code: {sales_response.status_code}")
        else:
            print("Login seems to have failed. Check the response content:")
            print(login_response.text[:500])  # Print first 500 chars of response
    else:
        print(f"Login failed with status code: {login_response.status_code}")

except requests.RequestException as e:
    print(f"An error occurred: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response headers: {dict(e.response.headers)}")