import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    # EX 9
    print(response.status_code)
    print(response.ok)
    print(response.url)
    print(response.encoding)

    # EX 10
    try:
        response.raise_for_status()

        time.sleep(1)
        missing = requests.get(
            BASE_URL + "/this-page-does-not-exist",
            timeout=TIMEOUT
        )
        missing.raise_for_status()
    except requests.HTTPError:
        print("Pagina nu exista sau a returnat o eroare HTTP.")

    # EX 11
    for name, value in response.headers.items():
        print(name, ":", value)

    # EX 12
    print(response.headers.get("Server", "lipseste"))
    print(response.headers.get("Content-Type", "lipseste"))
    print(response.headers.get("content-type", "lipseste"))

    # EX 13
    print(response.text.lower().count("cyber"))

    # EX 14
    html = response.text
    html_lower = html.lower()
    start = html_lower.find("<title>")

    if start != -1:
        start += len("<title>")
        end = html_lower.find("</title>", start)
        title = html[start:end].strip() if end != -1 else "Titlu negasit"
    else:
        title = "Titlu negasit"

    print(title)

    # EX 15
    lines = html.splitlines()
    print(len(lines))

    if lines:
        print(len(max(lines, key=len)))

    # EX 16
    if response.url.startswith("https://"):
        print("Conexiune securizata")
    else:
        print("Conexiune nesecurizata")

    # EX 17
    time.sleep(1)
    redirected = requests.get(
        "http://cybercor.org",
        timeout=TIMEOUT
    )

    for item in redirected.history:
        print(item.status_code, item.url)

    print(redirected.url)

    # EX 18
    time.sleep(1)
    head_response = requests.head(BASE_URL, timeout=TIMEOUT)

    time.sleep(1)
    get_response = requests.get(BASE_URL, timeout=TIMEOUT)

    print(len(head_response.content))
    print(len(get_response.content))

    # EX 19
    if response.cookies:
        for cookie in response.cookies:
            print(cookie.name, cookie.secure)
    else:
        print("Niciun cookie setat")

except requests.RequestException as e:
    print(e)

# EX 20
time.sleep(1)

try:
    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "WebLab-Student"
        })

        result = session.get(
            ECHO_URL + "/headers",
            timeout=TIMEOUT
        )

        result.raise_for_status()
        headers = result.json().get("headers", {})
        print(headers)

except (requests.RequestException, ValueError) as e:
    print(e)