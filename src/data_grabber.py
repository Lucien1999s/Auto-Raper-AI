import re
import requests
import logging
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from io import BytesIO

logging.basicConfig(level=logging.INFO)

def _read_online_pdf(url):
    try:
        response = requests.get(url)
        pdf_file = PdfReader(BytesIO(response.content))
        content = ""
        for page in range(len(pdf_file.pages)):
            content += pdf_file.pages[page].extract_text()
        content = re.sub(r'[\n]+', '', content)
        content = re.sub(r'[^\w\s]', '', content)
    except Exception as e:
        logging.info(f"Error reading PDF from {url}: {e}")
        return None

    return content

def get_data(query):
    url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={query}&btnG="
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    target_links = []
    links = soup.find_all('a')
    for link in links:
        href = link.get('href')
        if href and href.endswith('.pdf'):
            target_links.append(href)
    if len(target_links) > 5:
        target_links = target_links[:5]
    if not target_links:
        logging.warn("No paper match, please change your query keyword.")
        return None, None

    res = []
    failed_indices = []
    for i, link in enumerate(target_links):
        data = _read_online_pdf(link)
        if data is not None:
            res.append(data)
        else:
            failed_indices.append(i)

    # Remove the failed links from target_links
    for index in sorted(failed_indices, reverse=True):
        del target_links[index]

    return res, target_links  
