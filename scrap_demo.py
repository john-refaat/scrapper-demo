import requests
from bs4 import BeautifulSoup

# initialize the list of discovered urls
# with the first page to visit
urls = ["https://eg.hatla2ee.com"]

# until all pages have been visited
while len(urls) != 0:
    # get the page to visit from the list
    current_url = urls.pop()

    # crawling logic
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup)
    # extract new urls from the current page
    elements = soup.select("#UpperContent > div > div.newHome.home_section > div:nth-child(1) > div.newHomeHead > h1")
    for element in elements:
        print(element)


