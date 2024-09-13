import requests
from colorama import Fore, Style, init
import json
import time
import os  # For clearing terminal and setting title
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Load configuration
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# Print colored text
def print_colored(text, color):
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'aqua': Fore.CYAN,
        'white': Fore.WHITE
    }
    print(color_map.get(color, Fore.WHITE) + text + Style.RESET_ALL)

# Get current user time formatted as [HH:MM:SS]
def get_user_time():
    return datetime.now().strftime('%H:%M:%S')

# Fetch token using email and password
def fetch_token(email, password, use_proxy, proxy_list):
    url = "https://discord.com/api/v9/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Discord/1.0"
    }
    
    # Optionally use a proxy
    proxies = None
    if use_proxy and proxy_list:
        proxy = proxy_list.pop(0)  # Get the first proxy in the list
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        response.raise_for_status()
        data = response.json()
        if "token" in data:
            return data["token"]
        else:
            return None
    except requests.RequestException as e:
        print_colored(f"Error: {e}", "red")
        return None

# Load email:password pairs from accounts.txt
def load_accounts():
    with open('data/accounts.txt', 'r') as f:
        return [line.strip().split(':') for line in f.readlines()]

# Save valid tokens to tokens.txt in the format token | email
def save_token(token, email):
    with open('data/tokens.txt', 'a') as token_file:
        token_file.write(f"{token} | {email}\n")

# Mask the token for terminal display
def mask_token(token):
    """Display only the first few and last few characters of the token, masking the middle."""
    if len(token) > 10:
        return token[:6] + '...' + token[-6:]  # Show first 6 and last 6 characters
    return token

# Function to mask email
def mask_email(email):
    """Show the first part of the email and mask the last few characters before @."""
    name, domain = email.split('@')
    if len(name) > 3:
        masked_name = name[:-3] + '***'  # Keep the first part, mask last 3 characters
    else:
        masked_name = name + '***'  # If the name is shorter than 3 characters, mask fully
    return masked_name + '@' + domain

def main():
    # Set terminal title (Windows) and clear the terminal
    os.system('title Mass Token Fetcher - Legit Dark')  # For Windows
    os.system('cls' if os.name == 'nt' else 'clear')  # cls for Windows, clear for Linux/macOS
    
    # Load configuration and proxy list
    config = load_config()
    use_proxy = config.get('proxy', False)
    
    proxy_list = []
    if use_proxy:
        with open('data/proxies.txt', 'r') as proxy_file:
            proxy_list = [line.strip() for line in proxy_file.readlines()]

    # Load accounts and fetch tokens
    accounts = load_accounts()
    for email, password in accounts:
        masked_email = mask_email(email)  # Mask the email
        user_time = get_user_time()

        print(Fore.RED + f"[{user_time}] " + Fore.GREEN + "[+] " + Fore.CYAN + f"Fetching token for {masked_email}...")

        token = fetch_token(email, password, use_proxy, proxy_list)

        if token:
            masked_token = mask_token(token)  # Mask part of the token for display
            print_colored(Fore.RED + f"[{user_time}] " + Fore.GREEN + "[+] " + Fore.CYAN + f"Fetched token of {masked_email}, token saved at data/tokens.txt", "green")
            save_token(token, email)
        else:
            print_colored(Fore.CYAN + f"[{user_time}] " + Fore.RED + "[-] " + Fore.CYAN + f"Failed to fetch token for {masked_email}", "red")

        # Optional delay between requests to avoid rate limiting
        time.sleep(2)

if __name__ == "__main__":
    main()
