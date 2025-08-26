import time
import requests

URL = "http://localhost:8000/"

if __name__ == "__main__":
    print("Starting traffic generator. Press Ctrl+C to stop.")
    i = 0
    while True:
        try:
            r = requests.get(URL, timeout=2)
            print(f"{i} -> {r.status_code}: {r.text}")
        except Exception as e:
            print(f"{i} -> error: {e}")
        i += 1
        time.sleep(0.5)
