import csv
import hashlib
import json
import re
import socket
import ssl
import time

from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10
DIRECTORY = Path(__file__).resolve().parent

# EX 47
DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Student"
}


# EX 35
def parse_address(url: str) -> dict:
    """Descompune URL-ul."""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment
    }


# EX 36
def absolute_links(base: str, links: list) -> list:
    """Transforma linkurile in URL-uri complete."""
    return [urljoin(base.rstrip("/") + "/", link) for link in links]


# EX 39
class ImageFinder(HTMLParser):
    """Gaseste imaginile HTML."""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src is not None:
                self.images.append(src)


# EX 40
def page_fingerprint(url: str) -> str:
    """Calculeaza hashul SHA256."""
    time.sleep(1)
    response = requests.get(url, timeout=TIMEOUT, headers=DEFAULT_HEADERS)
    return hashlib.sha256(response.content).hexdigest()


# EX 41
def save_headers(response) -> dict:
    """Salveaza si citeste antetele JSON in lab_web_recon/headers.json."""
    headers_path = DIRECTORY / "headers.json"
    with open(headers_path, "w", encoding="utf-8") as f:
        json.dump(dict(response.headers), f, indent=2, ensure_ascii=False)

    with open(headers_path, "r", encoding="utf-8") as f:
        return json.load(f)


# EX 44
def fetch(url: str, timeout: int = TIMEOUT):
    """Descarca o pagina web."""
    time.sleep(1)
    return requests.get(
        url,
        timeout=timeout,
        headers=DEFAULT_HEADERS
    )


def get_status(url: str) -> int:
    """Returneaza codul HTTP."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul HTML."""
    lower = html.lower()
    start = lower.find("<title>")

    if start == -1:
        return "Titlu negasit"

    start += len("<title>")
    end = lower.find("</title>", start)

    if end == -1:
        return "Titlu negasit"

    return html[start:end].strip()


def security_headers(url: str, response=None) -> dict:
    """Verifica antetele de securitate."""
    if response is None:
        response = fetch(url)

    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    return {
        name: name in response.headers
        for name in names
    }


def score_headers(results: dict) -> str:
    """Calculeaza scorul antetelor."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Verifica mai multe cai HTTP."""
    results = {}

    for path in paths:
        url = urljoin(
            base.rstrip("/") + "/",
            path.lstrip("/")
        )

        try:
            results[path] = get_status(url)
        except requests.RequestException:
            results[path] = None

    return results


def fetch_robots(base: str):
    """Citeste robots.txt."""
    try:
        response = fetch(
            base.rstrip("/") + "/robots.txt"
        )
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

    return list(dict.fromkeys(paths))


# EX 37
def extract_links(html: str) -> list:
    """Extrage linkurile HTML."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


# EX 38
def split_links(links: list, domain: str) -> tuple:
    """Separa linkurile interne si externe."""
    base = domain if "://" in domain else "https://" + domain
    host = urlparse(base).hostname

    internal = []
    external = []

    for link in links:
        full_url = urljoin(
            base.rstrip("/") + "/",
            link
        )
        parsed = urlparse(full_url)

        if parsed.scheme not in ("http", "https"):
            continue

        if not parsed.hostname:
            continue

        if parsed.hostname.lower() == host.lower():
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


# EX 42
def resolve(hostname: str) -> str:
    """Returneaza adresa IP."""
    return socket.gethostbyname(hostname)


# EX 43
def cert_days_left(hostname: str) -> int:
    """Calculeaza zilele ramase ale certificatului."""
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443),
        timeout=TIMEOUT
    ) as sock:
        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_sock:
            expires = secure_sock.getpeercert()["notAfter"]

    timestamp = ssl.cert_time_to_seconds(expires)
    now = datetime.now(timezone.utc).timestamp()

    return int((timestamp - now) // 86400)


def redirect_chain(hostname: str) -> list:
    """Obtine lantul de redirectionari."""
    response = fetch("http://" + hostname)

    chain = []

    for item in response.history:
        chain.append({
            "status": item.status_code,
            "url": item.url
        })

    chain.append({
        "status": response.status_code,
        "url": response.url
    })

    return chain


# EX 49
def save_csv(results: dict):
    """Salveaza codurile HTTP in report.csv."""
    path = DIRECTORY / "report.csv"

    with open(
        path,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "path",
            "status",
            "checked_at"
        ])

        for relative_path, status in results.items():
            writer.writerow([
                relative_path,
                status,
                datetime.now().isoformat()
            ])

    return path


# EX 50
def site_report(url: str) -> dict:
    """Construieste raportul final al site-ului."""
    parsed = urlparse(url)

    if (
        parsed.scheme not in ("http", "https")
        or parsed.hostname != "cybercor.org"
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("URL nepermis")

    response = fetch(url)
    response.raise_for_status()

    # Salvare antete (EX 41)
    save_headers(response)

    title = get_title(response.text)
    host = urlparse(response.url).hostname

    try:
        ip = resolve(host)
    except OSError:
        ip = None

    try:
        redirects = redirect_chain(parsed.hostname)
    except requests.RequestException:
        redirects = []

    headers = security_headers(
        url,
        response=response
    )

    score = score_headers(headers)

    try:
        days = cert_days_left(host)
    except (OSError, ssl.SSLError, KeyError, ValueError):
        days = None

    links = extract_links(response.text)

    internal, external = split_links(
        links,
        response.url
    )

    robots = fetch_robots(BASE_URL)
    forbidden = disallowed_paths(robots)

    report = {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "title": title,
        "ip": ip,
        "redirects": redirects,
        "security_headers": headers,
        "security_score": score,
        "certificate_days": days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": forbidden
    }

    with open(
        DIRECTORY / "report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(response.status_code)
    print(response.url)
    print(title)
    print(ip)
    print(redirects)
    print(score)
    print(days)
    print(len(internal), len(external))
    print(forbidden)

    return report


# EX 46 + EX 49 + EX 50 (apeluri reparate)
if __name__ == "__main__":
    try:
        print("Status principal:", get_status(BASE_URL))

        # EX 49: generare report.csv
        rezultate_cai = check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml", "/inexistent"])
        cale_csv = save_csv(rezultate_cai)
        print("CSV salvat in:", cale_csv)

        # EX 41 + EX 50: generare headers.json si report.json
        site_report(BASE_URL)
        print("JSON salvat in:", DIRECTORY / "report.json")
    except (requests.RequestException, ValueError) as e:
        print(e)