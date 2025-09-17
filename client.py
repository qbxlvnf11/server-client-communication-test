import os
import requests
import time

# HOST = os.getenv("HOST", "localhost")
SERVER_HOSTNAME = os.getenv("SERVER_HOSTNAME", "localhost")
PORT = int(os.getenv("PORT", 8000))
URL = f"http://{SERVER_HOSTNAME}:{PORT}"

def run_test():
    print(f"Attempting to connect to server at [{URL}]...")
    try:
        response = requests.get(URL, timeout=5)
        response.raise_for_status()

        print("Connection successful!")
        print("─" * 20)
        print("Server Response:")
        print(response.json())
        print("─" * 20)

    except requests.exceptions.RequestException as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # time.sleep(3) 
    run_test()
