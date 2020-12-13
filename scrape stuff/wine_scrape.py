# Joseph Bentivegna Databases Assignment 2: Web Scraper

# Create a web scraper from a preapproved site and store the data in a NoSQL database.
# Datasets scraped should be "large". One should be able to ask the database a question about the scraped data, and receive an answer instantaneously.
# Submissions should include two parts; the code to scrape the site, queries to the new data

import requests
from bs4 import BeautifulSoup
import re
import math
import pymongo

color = 'White'

# first page of red wine list
page_prefix = "https://www.astorwines.com/"
new_page = "https://www.astorwines.com/WineSearchResult.aspx?p=1&search=Advanced&searchtype=Contains&term=&cat=1&color={}&Page=1".format(color)

print("Beginning scrape of", page_prefix)

# get url and parse it into a soup object
def get_and_parse_url(url):
    result = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)

# get individual wine urls from the main page
def get_wine_url(url):
    soup = get_and_parse_url(url)
    return([page_prefix + x.div.a.get('href') for x in soup.findAll("div", class_ = "item-teaser")])

# get number of pages of wine list
def get_number_of_pages(url):
    soup = get_and_parse_url(new_page)
    
    all_urls = []
    pagination_obj = soup.find("div", class_= "pagination hidden-xs col-sm-12").find_all("span")
    for span in pagination_obj:
        try:
            url_group = span.find_all("a")
            for url in url_group:
                all_urls.append(int(url.get('href').split("Page=")[1]))
        except:
            continue
            
    return(max(all_urls))
    
num_pages = get_number_of_pages(new_page)
print("Retrieved", str(num_pages), "pages to scrape")

# create list of all pages of wine
page_urls = []
for ii in range(0, num_pages):
    page_urls.append(new_page)
    new_page = page_urls[-1].split("Page=")[0] + "Page=" + str(int(page_urls[-1].split("Page=")[1]) + 1)
    
# create list of all individual wines on each page
wine_urls = []
for page in page_urls:
    wine_urls.extend(get_wine_url(page))
    
print("Retrieved", str(len(wine_urls)), "wines to scrape")

# create list of each wine object with scraped data
wines = []
for url in wine_urls:
    try:
        wine = {}

        soup = get_and_parse_url(url)

        # product name
        wine['name'] = soup.find("h1", class_ = "page-title").text

        # image url 
        wine['image_url'] = page_prefix[:-1] + soup.find("div", class_="item-portrait text-center").img.get("src")

        # tags
        wine['tags'] = [x.text for x in soup.find_all("div", class_ = re.compile("pill pill"))]

        # size
        wine['size'] = soup.find("span", class_ = "item-size-number pull-right text-muted").text

        # price (if on sale, find the sale price)
        try:
            wine['price'] = float(soup.find("span", class_ = "price-value price-bottle").text[1:])
        except:
            wine['price'] = float(soup.find("span", class_ = "price-value price-bottle price-sale").text[1:])

        # item information
        rows_we_want = ['Color', 'Vintage', 'Country', 'Region', 'Producer', 'Grape Variety']
        item_info = soup.find_all("div", class_="col-xs-12 col-md-4")
        for item in item_info:
            rows= item.find_all("div", class_="meta-group")
            for row in rows:
                try:
                    title = row.find("div", class_="meta-title").span.text
                    value = row.find("div", class_="meta-value").a.text

                    if title in rows_we_want:
                        wine[title] = value
                except:
                    continue

        wines.append(wine)
    
    except:
        continue
    
print('Collected', len(wines), 'wines\n')
print('Example Output:\n', wines[0])


# connect to the mongo cloud atlas database
username = input("username: ")
password = input("passord: ")
uri =   uri = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)
client = pymongo.MongoClient(uri)
db = client.wine_and_cheese.wine



# print(wines[0])

# insert the wines we scraped
try:
    db.insert_many(wines,ordered=False)
    print('Inserted', str(len(wines)), 'wines')
except:
    print('An error occurred - books were not stored to db')


