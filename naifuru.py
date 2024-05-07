import requests
from bs4 import BeautifulSoup
import os

def download_pdfs(base_url, folder_path):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    print(links)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for link in links:
        pdf_url = 'https://www.zisin.jp/publications/' + link
        pdf_response = requests.get(pdf_url, stream=True)
        if pdf_response.status_code == 200:
            filename = os.path.join(folder_path, link.split('/')[-1])
            with open(filename, 'wb') as f:
                for chunk in pdf_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f'Downloaded {filename}')
        else:
            print(f'Failed to download {pdf_url}')

# Usage example
download_pdfs('https://www.zisin.jp/publications/naifuru.html','./naifuru')