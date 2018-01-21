import os
import urllib.request
from bs4 import BeautifulSoup as bf


def get_html2soup(page_link):
    page_text = urllib.request.urlopen(page_link)
    soup = bf(page_text, "html.parser")
    return soup


def get_links(soup, keyword, link_head=""):
    links = []
    for link in soup.find_all('a'):
        href = link.get("href")
        if href != None and keyword in href:
            page_link = link_head + href
            links.append(page_link)

    return links

link_head = "https://github.com/"
link_start = "https://github.com/bioinformatics-core-shared-training/cruk-autumn-school-2017/tree/master/ChIP/Materials/Practicals"
keyword = "pdf"


first_page_soup = get_html2soup(link_start)
first_links = get_links(first_page_soup, keyword, link_head=link_head)

for link in first_links:
    print(link)
    os.system("wget %s" % link)
