import random, requests
import pandas as pd
from bs4 import BeautifulSoup

#Generate URL
def create_URL():
    search_ID = str(random.randint(1,99999999))
    full_URL = "https://www.goodreads.com/book/show/" + search_ID
    return full_URL

#Request HTML code from GoodReads
def ping_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

#Pull data from returned HTML code
def scrape_title(soup):
    title = soup.find(property = "og:title")
    return title["content"]

def scrape_author(soup):
    author = soup.find(property = "books:author")
    author = author["content"].split('.')
    author = author[len(author)-1].replace('_',' ')
    return author

def scrape_page_count(soup):
    page_count = soup.find(property = "books:page_count")
    return page_count["content"]

def scrape_num_reviews(soup):
    review_count = soup.find(itemprop = "reviewCount")
    return review_count["content"]

# Scrape program - pings sites and scrapes data
def scrape():
    total_scrapes = int(input("How many data points do you want to gather?"))
    #Create lists for storing scraped data
    #titles = []
    #authors = []
    page_counts = []
    counter = 1
    
    for i in range(total_scrapes):
        full_URL = create_URL()
        soup = ping_website(full_URL)

        #Try Except block to determine if page is valid
        while True:
            try:
                title = scrape_title(soup)
                break
            except TypeError:
                full_URL = create_URL()
                soup = ping_website(full_URL)
        
        #try:
        #    author = scrape_author(soup)
        #except TypeError:
        #    author = 'No Author'
        
        try:
            page_count = scrape_page_count(soup)
        except TypeError:
            page_count = 0

        #titles.append(title)
        #authors.append(author)
        page_counts.append(int(page_count))
        
        #Scrpaing Progress Counter (This method also you to overwrite the printout so you don't have a newline every pass)
        print(f"Pages scraped: {counter} of {total_scrapes}", end = '\r')
        counter += 1
    print()
    
    
    #print(titles)
    #print(authors)
    #print(page_counts)
    return page_counts

#Takes list of page counts and creates a data frame out of it
def build_dataframe(list_page_counts):
    data = {
        "Page Count" : list_page_counts
    }
    
    df = pd.DataFrame(data)
    
    return df

#Display Page Counts Frequencies in a Histogram
def display_histogram(dataframe):
    return df.hist()

def main():
    pages = scrape()
    df = build_dataframe(pages)
    display_histogram(df)

main()