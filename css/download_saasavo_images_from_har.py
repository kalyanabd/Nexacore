import re
from pathlib import Path
from urllib.parse import urlparse
import requests

IMAGE_URLS = """https://html.ditsolution.net/saasavo/images/logo.png
https://html.ditsolution.net/saasavo/images/demo-img/banner-diagram-img.png
https://html.ditsolution.net/saasavo/images/demo-img/band-img.png
https://html.ditsolution.net/saasavo/images/demo-img/band-img2.png
https://html.ditsolution.net/saasavo/images/demo-img/band-img3.png
https://html.ditsolution.net/saasavo/images/demo-img/band-img4.png
https://html.ditsolution.net/saasavo/images/demo-img/band-img5.png
https://html.ditsolution.net/saasavo/images/demo-img/band-img6.png
https://html.ditsolution.net/saasavo/images/demo-img/dashbord-thumb1.png
https://html.ditsolution.net/saasavo/images/demo-img/dashbord-thumb2.png
https://html.ditsolution.net/saasavo/images/demo-img/dashbord-thumb3.png
https://html.ditsolution.net/saasavo/images/demo-img/feature-thumb31.png
https://html.ditsolution.net/saasavo/images/demo-img/feature-shape31.png
https://html.ditsolution.net/saasavo/images/demo-img/feature-thumb32.png
https://html.ditsolution.net/saasavo/images/demo-img/feature-shape32.png
https://html.ditsolution.net/saasavo/images/demo-img/feature-thumb33.png
https://html.ditsolution.net/saasavo/images/demo-img/check.png
https://html.ditsolution.net/saasavo/images/demo-img/feat-ai-line.png
https://html.ditsolution.net/saasavo/images/demo-img/feature-shape33.png
https://html.ditsolution.net/saasavo/images/demo-img/process-icon1.png
https://html.ditsolution.net/saasavo/images/demo-img/process-icon2.png
https://html.ditsolution.net/saasavo/images/demo-img/process-icon3.png
https://html.ditsolution.net/saasavo/images/demo-img/process-shape1.png
https://html.ditsolution.net/saasavo/images/demo-img/process-shape2.png
https://html.ditsolution.net/saasavo/images/demo-img/integration-thumb21.png
https://html.ditsolution.net/saasavo/images/demo-img/about-effient21.png
https://html.ditsolution.net/saasavo/images/demo-img/project-thumb1.png
https://html.ditsolution.net/saasavo/images/demo-img/project-thumb2.png
https://html.ditsolution.net/saasavo/images/demo-img/project-thumb3.png
https://html.ditsolution.net/saasavo/images/demo-img/accrodion-effient.png
https://html.ditsolution.net/saasavo/images/demo-img/accrodion-shape1.png
https://html.ditsolution.net/saasavo/images/demo-img/accrodion-shape2.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-quote.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-autor1.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-autor2.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-autor3.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-two-effient.png
https://html.ditsolution.net/saasavo/images/demo-img/pricing-icon.png
https://html.ditsolution.net/saasavo/images/demo-img/pricing-check.png
https://html.ditsolution.net/saasavo/images/demo-img/pricing-box3.png
https://html.ditsolution.net/saasavo/images/demo-img/pricing-top3.png
https://html.ditsolution.net/saasavo/images/demo-img/blog-thumb1.png
https://html.ditsolution.net/saasavo/images/demo-img/blog-thumb2.png
https://html.ditsolution.net/saasavo/images/demo-img/blog-thumb3.png
https://html.ditsolution.net/saasavo/images/demo-img/blog-top-eff.png
https://html.ditsolution.net/saasavo/images/footer-logo2.png
https://html.ditsolution.net/saasavo/images/demo-img/banner-bg3.png
https://html.ditsolution.net/saasavo/images/demo-img/brand-line1.png
https://html.ditsolution.net/saasavo/images/demo-img/brand-line2.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-box-eff1.png
https://html.ditsolution.net/saasavo/images/demo-img/testi-box-eff2.png
https://html.ditsolution.net/saasavo/images/demo-img/footer-bg2.png""".strip().splitlines()

OUTPUT_DIR = Path.cwd()

def local_path(url: str) -> Path:
    parsed = urlparse(url)
    marker = "/saasavo/"
    path = parsed.path
    if marker in path:
        path = path.split(marker, 1)[1]
    return OUTPUT_DIR / path.lstrip("/")

def download(url: str):
    path = local_path(url)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 0:
        print(f"SKIP: {path}")
        return

    print(f"GET : {url}")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    path.write_bytes(r.content)
    print(f"SAVE: {path}")

def main():
    for url in IMAGE_URLS:
        try:
            download(url)
        except Exception as e:
            print(f"FAIL: {url} -> {e}")

    print("\nDone. Images saved inside your project images/ folder.")

if __name__ == "__main__":
    main()
