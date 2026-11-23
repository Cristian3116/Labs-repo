import time
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


# EX 21
def fetch(url: str, timeout: int = 10):
    """Returneaza raspunsul HTTP."""
    time.sleep(1)
    return requests.get(url, timeout=timeout)


# EX 22
def get_status(url: str) -> int:
    """Returneaza codul HTTP."""
    return fetch(url).status_code


# EX 23
def fetch_timeout(url: str, timeout: int = 10):
    """Foloseste un timeout implicit sau explicit."""
    return fetch(url, timeout=timeout)


# EX 24
def get_title(html: str) -> str:
    """Extrage titlul paginii HTML."""
    lower = html.lower()
    start = lower.find("<title>")

    if start == -1:
        return "Titlu negasit"

    start += len("<title>")
    end = lower.find("</title>", start)

    if end == -1:
        return "Titlu negasit"

    return html[start:end].strip()


# EX 25
def show_docstring():
    """Afiseaza documentatia functiei get_title."""
    help(get_title)


# EX 26
def check_type_hints():
    """Verifica comportamentul adnotarilor de tip."""
    try:
        return get_status(123)
    except (requests.RequestException, TypeError, ValueError):
        return None


# EX 27
def page_exists(url: str) -> bool:
    """Verifica existenta paginii."""
    try:
        response = fetch(url)
        return response.ok
    except requests.RequestException:
        return False


# EX 28
def check_paths(base: str, paths: list) -> dict:
    """Returneaza codurile HTTP pentru cai."""
    results = {}

    for path in paths:
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None

    return results


# EX 29
def get_header(url: str, name: str, default="lipseste"):
    """Returneaza un antet HTTP."""
    response = fetch(url)
    return response.headers.get(name, default)


# EX 30
def security_headers(url: str) -> dict:
    """Verifica antetele de securitate."""
    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    response = fetch(url)
    results = {}

    for name in names:
        results[name] = name in response.headers

    return results


# EX 31
def score_headers(results: dict) -> str:
    """Returneaza scorul antetelor."""
    return f"{sum(results.values())}/{len(results)}"


# EX 32
def fetch_robots(base: str):
    """Descarca robots.txt."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text) -> list:
    """Extrage valorile Disallow."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()

            if path:
                paths.append(path)

    return paths


# EX 33
def response_times(*urls: str) -> dict:
    """Returneaza timpul fiecarei cereri."""
    results = {}

    for url in urls:
        try:
            response = fetch(url)
            results[url] = response.elapsed.total_seconds()
        except requests.RequestException:
            results[url] = None

    return results


# EX 34
def log(message: str, **details):
    """Afiseaza mesajul si detaliile."""
    result = message

    for key, value in details.items():
        result += f" | {key}={value}"

    print(result)


def safe_call(function, *args, **kwargs):
    """Trateaza erorile cererilor."""
    try:
        return function(*args, **kwargs)
    except (requests.RequestException, TypeError, ValueError) as e:
        print(e)
        return None


if __name__ == "__main__":
    # EX 21
    response = safe_call(fetch, BASE_URL)
    if response is not None:
        print(response.status_code)

    # EX 22
    for path in ["/", "/robots.txt", "/sitemap.xml"]:
        print(path, safe_call(get_status, BASE_URL + path))

    # EX 23
    response1 = safe_call(fetch_timeout, BASE_URL)
    response2 = safe_call(fetch_timeout, BASE_URL, timeout=3)
    if response1 is not None:
        print(response1.status_code)
    if response2 is not None:
        print(response2.status_code)

    # EX 24
    if response is not None:
        print(get_title(response.text))

    # EX 25
    show_docstring()

    # EX 26
    print(check_type_hints())

    # EX 27
    print(page_exists("https://this-domain-does-not-exist.invalid"))

    # EX 28
    print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

    # EX 29
    print(safe_call(get_header, BASE_URL, name="Server"))

    # EX 30
    headers = safe_call(security_headers, BASE_URL)
    print(headers)

    # EX 31
    if headers is not None:
        print(score_headers(headers))

    # EX 32
    robots = fetch_robots(BASE_URL)
    print(disallowed_paths(robots))
    print(disallowed_paths(None))

    # EX 33
    print(response_times(BASE_URL, BASE_URL + "/robots.txt"))

    # EX 34
    log("verificat", url=BASE_URL, status=200)