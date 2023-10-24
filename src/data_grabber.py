import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from PyPDF2 import PdfReader
from io import BytesIO

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
        print(f"Error reading PDF from {url}: {e}")
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
        return "No paper match, please change your query keyword."
    
    res = []
    failed_indices = []
    for i, link in enumerate(tqdm(target_links, desc="Downloading papers")):
        data = _read_online_pdf(link)
        if data is not None:
            res.append(data)
        else:
            failed_indices.append(i)

    # Remove the failed links from target_links
    for index in sorted(failed_indices, reverse=True):
        del target_links[index]

    return res, target_links


