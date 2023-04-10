import datetime
import re
from typing import List

from bs4 import BeautifulSoup

from dancesport_parser.util import parseHtml
from dancesport_parser.o2cm.model import Competition

def parseMain(htmlDOM: BeautifulSoup = None, rawHtml: str = None) -> List[Competition]:
    """Parse o2cm main results screen, i.e. results.o2cm.com.
    
    Keyword arguments:
    htmlDOM -- HTML contents to parse.
    rawHtml -- If `htmlDOM` is unspecified, raw string to directly parse.
    """
    if htmlDOM is None and rawHtml is None:
        raise RuntimeError("Expected either htmlDOM or rawHtml to be provided.")
    
    if htmlDOM is None:
        htmlDOM = parseHtml(rawHtml)

    results: List[Competition] = []
    competitionsTable = htmlDOM.find_all("table", id="main_tbl")[0]
    yearInput = htmlDOM.find_all('input', id='inyear')[0]
    year = int(yearInput['value'])
    for row in competitionsTable.find_all("tr"):
        rowData = row.find_all("td")
        if rowData is None or len(rowData) == 0:
            continue

        if "class" in rowData[0].attrs and rowData[0]["class"][0] == "h3":
            year = int(rowData[0].get_text().strip())
        elif "class" in row.attrs and row["class"][0] == "t1n":
            date = str(rowData[0].get_text().strip())
            compName = rowData[1].get_text().strip()
            compUrl = row.find("a")["href"]
            matchCompUrl = re.match(r'event[23].asp\?event=([a-zA-Z]{0,4}\d{0,5}[a-zA-Z]?)&.*', compUrl)
            compId = matchCompUrl.group(1).lower()
            fullDate = date + " " + str(year)
            compDate = datetime.datetime.strptime(fullDate, "%b %d %Y").date()
            competition = Competition(compId, compName, compDate)
            results.append(competition)
    return results