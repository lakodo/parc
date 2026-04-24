import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SITEMAP = "https://www.edfenergy.com/sitemap.xml"
PDF_PREFIX = "https://www.edfenergy.com/sites/default/files"

CHECKED_PAGES_FILE = Path("checked_pages.txt")
PDFS_FILE = Path("edf_public_pdfs.txt")

HEADERS = {
    "User-Agent": "Mozilla/5.0 PDF-link-collector/1.0"
}

session = requests.Session()
session.headers.update(HEADERS)


def load_set(path):
    if not path.exists():
        return set()
    return set(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def append_line(path, value):
    with path.open("a", encoding="utf-8") as f:
        f.write(value + "\n")


def fetch(url):
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.text


def parse_sitemap(url):
    xml_text = fetch(url)
    root = ET.fromstring(xml_text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    urls = []

    for loc in root.findall(".//sm:url/sm:loc", ns):
        urls.append(loc.text.strip())

    for loc in root.findall(".//sm:sitemap/sm:loc", ns):
        child_sitemap = loc.text.strip()
        print(f"Reading child sitemap: {child_sitemap}")
        urls.extend(parse_sitemap(child_sitemap))

    return urls


def extract_pdf_links_from_page(page_url):
    html = fetch(page_url)
    soup = BeautifulSoup(html, "html.parser")

    pdfs = set()

    for a in soup.find_all("a", href=True):
        href = urljoin(page_url, a["href"])
        clean = href.split("#")[0]

        if ".pdf" in clean.lower() and clean.startswith(PDF_PREFIX):
            pdfs.add(clean)

    return pdfs


checked_pages = load_set(CHECKED_PAGES_FILE)
known_pdfs = load_set(PDFS_FILE)

page_urls = parse_sitemap(SITEMAP)
page_urls = sorted(set(page_urls))

print(f"Pages in sitemap: {len(page_urls)}")
print(f"Already checked pages: {len(checked_pages)}")
print(f"Already known PDFs: {len(known_pdfs)}")

for i, url in enumerate(page_urls, 1):
    if url in checked_pages:
        print(f"[{i}/{len(page_urls)}] Skipping already checked: {url}")
        continue

    print(f"[{i}/{len(page_urls)}] Checking: {url}")

    try:
        clean_url = url.split("#")[0]

        if ".pdf" in clean_url.lower() and clean_url.startswith(PDF_PREFIX):
            if clean_url not in known_pdfs:
                known_pdfs.add(clean_url)
                append_line(PDFS_FILE, clean_url)
        else:
            found_pdfs = extract_pdf_links_from_page(url)

            for pdf in sorted(found_pdfs):
                if pdf not in known_pdfs:
                    known_pdfs.add(pdf)
                    append_line(PDFS_FILE, pdf)
                    print(f"  Found PDF: {pdf}")

        checked_pages.add(url)
        append_line(CHECKED_PAGES_FILE, url)

        time.sleep(0.1)

    except Exception as e:
        print(f"  Error: {e}")
        print("  Not marking as checked, will retry next run.")

print(f"Done. Total known PDFs: {len(known_pdfs)}")
