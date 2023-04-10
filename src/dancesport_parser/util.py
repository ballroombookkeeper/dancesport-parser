from bs4 import BeautifulSoup
from tidylib import tidy_document

def parseHtml(rawHtml: str) -> BeautifulSoup:
    tidiedPage, _ = tidy_document(rawHtml)
    return BeautifulSoup(tidiedPage, "html.parser")