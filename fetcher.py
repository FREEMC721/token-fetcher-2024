import os
import sys
import time
import requests
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

# Function to print colored text
def print_colored(text, color):
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'aqua': Fore.CYAN,
        'white': Fore.WHITE
    }
    print(color_map.get(color, Fore.WHITE) + text + Style.RESET_ALL)

# Fetch the token using email and password
def fetch_token(email, password):
    url = "https://discord.com/api/v9/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Discord/1.0"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if "token" in data:
            return data["token"]
        else:
            return None
    except requests.RequestException as e:
        print_colored(f"Error: {e}", "red")
        return None

# Mask the token for terminal display
def mask_token(token):
    """Show only the first and last few characters of the token, masking the middle."""
    if len(token) > 10:
        return token[:6] + '...' + token[-6:]
    return token

# Save the full token to tokens.txt
def save_token(token):
    with open('token.txt', 'a') as token_file:
        token_file.write(token + '\n')

# Get the current time formatted as HH:MM:SS
def get_current_time():
    return datetime.now().strftime('%H:%M:%S')

# Clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Set the terminal window title
def set_terminal_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')
    else:
        sys.stdout.write(f'\033]0;{title}\a')
        sys.stdout.flush()

def main():
    # Display the ASCII art in aqua
    ascii_art = """
    █████▒▓█████▄▄▄█████▓ ▄████▄   ██░ ██ ▓█████  ██▀███  
    ▓██   ▒ ▓█   ▀▓  ██▒ ▓▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▓██ ▒ ██▒
    ▒████ ░ ▒███  ▒ ▓██░ ▒░▒▓█    ▄ ▒██▀▀██░▒███   ▓██ ░▄█ ▒
    ░▓█▒  ░ ▒▓█  ▄░ ▓██▓ ░ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒██▀▀█▄  
    ░▒█░    ░▒████▒ ▒██▒ ░ ▒ ▓███▀ ░░▓█▒░██▓░▒████▒░██▓ ▒██▒
     ▒ ░    ░░ ▒░ ░ ▒ ░░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒▓ ░▒▓░
     ░       ░ ░  ░   ░      ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░▒ ░ ▒░
     ░ ░       ░    ░      ░         ░  ░░ ░   ░     ░░   ░
    """
    print_colored(ascii_art, "aqua")

    # Clear the terminal and set the title
    time.sleep(2)  # Optional pause to display ASCII art
    clear_terminal()
    set_terminal_title("DISCORD TOKEN FETCHER - LEGIT DARK")

    # Prompt user for email and password
    email = input(Fore.RED + f"[{get_current_time()}] " + Fore.GREEN + "[+] " + Fore.CYAN + "Email: " + Fore.WHITE)
    password = input(Fore.RED + f"[{get_current_time()}] " + Fore.GREEN + "[+] " + Fore.CYAN + "Password: " + Fore.WHITE)

    # Fetch the token
    token = fetch_token(email, password)

    # Print the result and save token
    if token:
        masked_token = mask_token(token)  # Mask the token for terminal output
        print_colored(f"[+] Successfully fetched token, token saved at token.txt", "green")
        save_token(token)  # Save full token to tokens.txt
    else:
        print_colored("Failed to fetch token.", "red")

if __name__ == "__main__":
    main()


