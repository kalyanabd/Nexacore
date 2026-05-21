import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://html.ditsolution.net/saasavo/"
BASE_PATH = urlparse(BASE_URL).path
OUTPUT_DIR = Path.cwd()
HTML_PAGES = ["", "about.html", "service.html", "service-details.html", "contact.html"]

ASSET_URL_RE = re.compile(r"url\((?:['\"]?)([^)'\"]+)(?:['\"]?)\)")


def is_local_asset(url: str) -> bool:
    if not url:
        return False
    url = url.strip()
    return not (url.startswith("http://") or url.startswith("https://") or url.startswith("//") or url.startswith("data:") or url.startswith("mailto:") or url.startswith("tel:") or url.startswith("#"))


def normalize_asset_path(url: str) -> str:
    path = url.strip().strip('"\'')
    path = path.split("#", 1)[0].split("?", 1)[0]
    path = path.lstrip("./")
    while path.startswith("../"):
        path = path[3:]
    return path


def local_path_for_url(full_url: str) -> str:
    parsed = urlparse(full_url)
    path = parsed.path
    if BASE_PATH and path.startswith(BASE_PATH):
        path = path[len(BASE_PATH):]
    return path.lstrip("/")


def download_file(remote_path: str, output_path: Path, base_url: str = BASE_URL) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    full_url = urljoin(base_url, remote_path)
    print(f"Downloading {full_url} -> {output_path}")
    response = requests.get(full_url, timeout=20)
    response.raise_for_status()
    output_path.write_bytes(response.content)


def find_html_assets(html_text: str) -> set[str]:
    soup = BeautifulSoup(html_text, "html.parser")
    assets = set()
    for tag in soup.find_all(["link", "script", "img"]):
        if tag.name == "link" and tag.get("href"):
            assets.add(tag["href"])
        elif tag.name == "script" and tag.get("src"):
            assets.add(tag["src"])
        elif tag.name == "img" and tag.get("src"):
            assets.add(tag["src"])
    return assets


def find_css_assets(css_text: str) -> set[str]:
    assets = set()
    for match in ASSET_URL_RE.findall(css_text):
        asset = match.strip().strip('"\'')
        if is_local_asset(asset):
            assets.add(asset)
    return assets


def download_assets_from_html(html_path: Path) -> None:
    html_text = html_path.read_text(encoding="utf-8")
    asset_urls = find_html_assets(html_text)
    downloaded = set()
    css_paths = []

    for url in asset_urls:
        if not is_local_asset(url):
            continue
        full_url = urljoin(BASE_URL, url)
        local_path = local_path_for_url(full_url)
        if not local_path:
            continue
        output_path = OUTPUT_DIR / local_path
        if output_path in downloaded:
            continue
        download_file(url, output_path)
        downloaded.add(output_path)
        if output_path.suffix.lower() == ".css":
            css_paths.append(output_path)

    for css_path in css_paths:
        css_text = css_path.read_text(encoding="utf-8", errors="ignore")
        css_base_url = urljoin(BASE_URL, str(css_path.relative_to(OUTPUT_DIR)).replace('\\\\', '/'))
        for css_url in find_css_assets(css_text):
            if not is_local_asset(css_url):
                continue
            full_css_url = urljoin(css_base_url, css_url)
            local_path = local_path_for_url(full_css_url)
            if not local_path:
                continue
            output_path = OUTPUT_DIR / local_path
            if output_path in downloaded:
                continue
            download_file(full_css_url, output_path, base_url="")
            downloaded.add(output_path)


def save_industries_section() -> None:
    response = requests.get(BASE_URL, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    section = soup.find("div", class_="accordion-section-one")
    if section is None:
        raise RuntimeError("Industries section not found in the main page")

    html = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <title>Industries</title>
    <link href=\"css/bootstrap.min.css\" rel=\"stylesheet\">
    <link href=\"css/style.css\" rel=\"stylesheet\">
    <link href=\"css/responsive.css\" rel=\"stylesheet\">
  </head>
  <body>
"""
    html += str(section)
    html += "\n  </body>\n</html>\n"
    industries_output = OUTPUT_DIR / "industries.html"
    industries_output.write_text(html, encoding="utf-8")
    print(f"Saved industries section to {industries_output.name}")


def main() -> None:
    for page_path in HTML_PAGES:
        output_name = "index.html" if page_path == "" else page_path
        output_path = OUTPUT_DIR / output_name
        page_url = urljoin(BASE_URL, page_path)
        print(f"Downloading HTML page {page_url} -> {output_path.name}")
        response = requests.get(page_url, timeout=20)
        response.raise_for_status()
        output_path.write_text(response.text, encoding="utf-8")
        download_assets_from_html(output_path)

    save_industries_section()
    print("Done. Saved extracted pages and assets:")
    for page_path in HTML_PAGES:
        print(f" - {'index.html' if page_path == '' else page_path}")
    print(" - industries.html")


if __name__ == "__main__":
    main()
