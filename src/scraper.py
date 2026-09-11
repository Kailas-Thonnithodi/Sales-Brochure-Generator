from bs4 import BeautifulSoup
from urllib.parse import urldefrag, urljoin, urlparse
import requests


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]

def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    hrefs = [link.get("href") for link in soup.find_all("a")]
    # resolve relative hrefs against the page, drop the #fragment, keep only http(s),
    # and de-duplicate while preserving order
    seen = {}
    for href in hrefs:
        if not href:
            continue
        link = urldefrag(urljoin(url, href)).url
        if urlparse(link).scheme in ("http", "https"):
            seen[link] = None
    return list(seen)
