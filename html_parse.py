from bs4 import BeautifulSoup

def parse(html):
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()