import re
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://html.ditsolution.net/saasavo/"
OUTPUT_DIR = Path.cwd()

HTML_PAGES = [
    "",
    "about.html",
    "service.html",
    "service-details.html",
    "contact.html",
]

URL_RE = re.compile(r"url\(\s*['\"]?([^)'\"\s]+)['\"]?\s*\)", re.I)
IMPORT_RE = re.compile(r"@import\s+(?:url\()?['\"]?([^)'\";]+)['\"]?\)?", re.I)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
})

downloaded_urls: set[str] = set()


def is_skip_url(url: str) -> bool:
    if not url:
        return True

    url = url.strip()
    return (
        url.startswith("#")
        or url.startswith("data:")
        or url.startswith("mailto:")
        or url.startswith("tel:")
        or url.startswith("javascript:")
    )


def is_same_site(url: str) -> bool:
    parsed_base = urlparse(BASE_URL)
    parsed_url = urlparse(urljoin(BASE_URL, url))
    return parsed_base.netloc == parsed_url.netloc


def clean_url(url: str) -> str:
    url = url.strip().strip("'\"")
    url = url.split("#", 1)[0]
    return url


def local_output_path(full_url: str) -> Path:
    parsed_base = urlparse(BASE_URL)
    parsed = urlparse(full_url)

    base_path = parsed_base.path.rstrip("/") + "/"
    path = unquote(parsed.path)

    if path.startswith(base_path):
        path = path[len(base_path):]
    else:
        path = path.lstrip("/")

    if not path or path.endswith("/"):
        path = path + "index.html"

    return OUTPUT_DIR / path


def download_url(url: str, referer: str = BASE_URL) -> Path | None:
    if is_skip_url(url):
        return None

    full_url = urljoin(referer, clean_url(url))

    if not is_same_site(full_url):
        return None

    if full_url in downloaded_urls:
        return local_output_path(full_url)

    downloaded_urls.add(full_url)
    output_path = local_output_path(full_url)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading: {full_url} -> {output_path.relative_to(OUTPUT_DIR)}")

    try:
        response = session.get(full_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"  FAILED: {full_url} ({e})")
        return None

    output_path.write_bytes(response.content)

    suffix = output_path.suffix.lower()
    if suffix == ".css":
        parse_css_assets(output_path, full_url)
    elif suffix == ".js":
        parse_js_assets(output_path, full_url)

    return output_path


def extract_srcset(value: str) -> list[str]:
    urls = []
    for item in value.split(","):
        part = item.strip().split(" ")[0]
        if part:
            urls.append(part)
    return urls


def parse_html_assets(html_path: Path, page_url: str) -> None:
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    attrs = [
        "src",
        "href",
        "data-src",
        "data-bg",
        "data-background",
        "data-image",
        "poster",
    ]

    for tag in soup.find_all(True):
        for attr in attrs:
            value = tag.get(attr)
            if value:
                download_url(value, page_url)

        if tag.get("srcset"):
            for src in extract_srcset(tag["srcset"]):
                download_url(src, page_url)

        if tag.get("data-srcset"):
            for src in extract_srcset(tag["data-srcset"]):
                download_url(src, page_url)

        if tag.get("style"):
            for asset in URL_RE.findall(tag["style"]):
                download_url(asset, page_url)

    # Also catch any inline CSS inside <style> tags
    for style_tag in soup.find_all("style"):
        css_text = style_tag.get_text()
        parse_css_text(css_text, page_url)


def parse_css_text(css_text: str, css_url: str) -> None:
    for imported in IMPORT_RE.findall(css_text):
        download_url(imported, css_url)

    for asset in URL_RE.findall(css_text):
        download_url(asset, css_url)


def parse_css_assets(css_path: Path, css_url: str) -> None:
    css_text = css_path.read_text(encoding="utf-8", errors="ignore")
    parse_css_text(css_text, css_url)


def parse_js_assets(js_path: Path, js_url: str) -> None:
    """
    Many templates reference images inside JS strings.
    This catches common relative image/font paths from JS files.
    """
    js_text = js_path.read_text(encoding="utf-8", errors="ignore")

    possible_assets = re.findall(
        r"""['"]([^'"]+\.(?:png|jpg|jpeg|webp|gif|svg|css|js|woff|woff2|ttf|eot|mp4|webm))['"]""",
        js_text,
        flags=re.I,
    )

    for asset in possible_assets:
        download_url(asset, js_url)


def save_page(page_path: str) -> Path:
    page_url = urljoin(BASE_URL, page_path)
    output_name = "index.html" if page_path == "" else page_path
    output_path = OUTPUT_DIR / output_name

    print(f"\nDownloading page: {page_url} -> {output_name}")
    response = session.get(page_url, timeout=30)
    response.raise_for_status()
    output_path.write_text(response.text, encoding="utf-8")

    parse_html_assets(output_path, page_url)
    return output_path


def save_industries_page() -> None:
    """
    Your old script extracted FAQ as industries by mistake.
    This creates a real industries page from the service page structure if no
    dedicated industries page exists in the template.
    """
    industries_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Industries - Nexacore</title>
<link href="css/bootstrap.min.css" rel="stylesheet">
<link href="css/style.css" rel="stylesheet">
<link href="css/responsive.css" rel="stylesheet">
<link rel="shortcut icon" href="images/favicon.png" type="image/x-icon">
<link rel="icon" href="images/favicon.png" type="image/x-icon">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<div class="page-wrapper">
<section class="service-section-one" style="padding:100px 0;">
  <div class="auto-container">
    <div class="sec-title text-center">
      <div class="section-sub-title">
        <h5 class="sub-title">Industries</h5>
      </div>
      <div class="section-title">
        <h1 class="title">Industries We Serve</h1>
      </div>
      <div class="section-desc">
        <p>Nexacore builds AI, cloud, and digital solutions for modern businesses.</p>
      </div>
    </div>

    <div class="row">
      <div class="col-xl-4 col-lg-6 col-md-6">
        <div class="single-service-box">
          <div class="service-content">
            <h3>Banking & Finance</h3>
            <p>AI compliance, document automation, risk analysis, and customer support systems.</p>
          </div>
        </div>
      </div>

      <div class="col-xl-4 col-lg-6 col-md-6">
        <div class="single-service-box">
          <div class="service-content">
            <h3>Healthcare</h3>
            <p>Secure digital workflows, analytics dashboards, and AI-assisted operations.</p>
          </div>
        </div>
      </div>

      <div class="col-xl-4 col-lg-6 col-md-6">
        <div class="single-service-box">
          <div class="service-content">
            <h3>Retail & E-Commerce</h3>
            <p>Customer insights, intelligent recommendations, automation, and scalable platforms.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
</div>
<script src="js/jquery.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/main.js"></script>
</body>
</html>
"""
    (OUTPUT_DIR / "industries.html").write_text(industries_html, encoding="utf-8")
    print("Saved industries.html")


def main() -> None:
    for page in HTML_PAGES:
        save_page(page)

    save_industries_page()

    print("\nDone. Extracted pages:")
    print(" - index.html")
    for page in HTML_PAGES[1:]:
        print(f" - {page}")
    print(" - industries.html")


if __name__ == "__main__":
    main()
