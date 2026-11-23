import time
import urllib.request
import requests
from requests import get
import requests as rq

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# EX 1
print(requests.__version__)

# EX 2
try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)

    time.sleep(1)
    response = get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
except requests.RequestException as e:
    print(e)

# EX 3
time.sleep(1)
try:
    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
except requests.RequestException as e:
    print(e)

# EX 4
time.sleep(1)
try:
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
        print(response.status)
        html = response.read().decode("utf-8", errors="replace")
        print(html[:200])
except Exception as e:
    print(e)

# EX 5
print(dir(requests))

# EX 6
help(requests.get)

time.sleep(1)
try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
except requests.RequestException as e:
    print(e)

# EX 7
time.sleep(1)
try:
    start = time.perf_counter()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    end = time.perf_counter()

    print(end - start)
    print(response.elapsed.total_seconds())
except requests.RequestException as e:
    print(e)

# EX 8
try:
    import bs4
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")