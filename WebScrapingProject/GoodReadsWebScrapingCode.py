import random, requests
import pandas as pd
from bs4 import BeautifulSoup

#Create the URL with a randomly generated search ID.
def create_URL():
    search_ID = str(random.randint(1,99999999))
    full_URL = "https://www.goodreads.com/book/show/" + search_ID
    return full_URL

#Request HTML code from GoodReads using the created URL.
def ping_website(url):
    #Get HTML code from website.
    response = requests.get(url)
    #Parse out text of HTML code.
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

#Extract book title from HTML code.
def scrape_title(soup):
    #Use property ID og:title to find book title
    title = soup.find(property = "og:title")
    #Extract title from line of HTML code.
    return title["content"]

#Extract primary author from HTML code.
def scrape_author(soup):
    #Use property ID books:author to find first mentioned author.
    author = soup.find(property = "books:author")
    #Break HTML line into a list of strings by spliting on any period.  Author will be the last item in the list.
    author = author["content"].split('.')
    #Extract author name from the list and replace the underscore with a space to properly format the name.
    author = author[len(author)-1].replace('_',' ')
    return author

#Extract page count from HTML code.
def scrape_page_count(soup):
    #Use property ID books:page_count to find the page count.
    page_count = soup.find(property = "books:page_count")
    #Extract page count from line of HTML code.
    return page_count["content"]

#Extract number of reviews from HTML code.
def scrape_num_reviews(soup):
    #Use itemprop ID reviewCount to find the number of reviews done for the book.
    review_count = soup.find(itemprop = "reviewCount")
    return review_count["content"]

#Get HTML code from GoodReads and extract data points from each page.
def scrape():
    #User inputs how many books they want to scrape data from.
    total_scrapes = int(input("How many data points do you want to gather?"))
    #Create lists for storing scraped data
    #titles = []
    #authors = []
    page_counts = []
    #Counter to keep track of how many books have been scrapped.
    counter = 1
    
    #Loop to request new webpages and scrape data from them.  Will iterate the number of times the user input.
    for i in range(total_scrapes):
        #Ceate an initial URL.
        full_URL = create_URL()
        #Use URL to request a webpage.
        soup = ping_website(full_URL)

        #Try Except block to determine if page is valid
        while True:
            try:
                #An invalid or broken webpage won't have the property ID needed and will throw a TypeError.
                title = scrape_title(soup)
                break
            except TypeError:
                #If the webpage is broken, generate a new URL and try again.
                full_URL = create_URL()
                soup = ping_website(full_URL)
        
        #try:
        #    author = scrape_author(soup)
        #except TypeError:
        #    author = 'No Author'
        
        #Try to extract a page count from the current webpage.
        try:
            page_count = scrape_page_count(soup)
        #If no page out is found, set it to 0.
        except TypeError:
            page_count = 0

        #titles.append(title)
        #authors.append(author)
        
        #Add to a running list of integers representing the scraped page counts.
        page_counts.append(int(page_count))
        
        #Scraping Progress Counter (This method allows you to overwrite the printout so you don't have a newline every pass).
        print(f"Pages scraped: {counter} of {total_scrapes}", end = '\r')
        #Increment counter by 1.
        counter += 1
    print()
    
    #Return the list of page counts scraped.
    return page_counts

#Takes list of page counts and creates a data frame out of it
def build_dataframe(list_page_counts):
    #Build a dictionary with the Key Page Count and the value the list of page counts compiled.
    data = {
        "Page Count" : list_page_counts
    }
    
    #Create a dataframe out of this newly created dictionary.
    df = pd.DataFrame(data)
    
    #Return the newly created dataframe.
    return df

#Display Page Counts Frequencies in a Histogram using the newly created dataframe.
def display_histogram(dataframe):
    return dataframe.hist()

def main():
    #Scrapes webpages and builds a list of each books page counts.
    pages = scrape()
    #Creates a dataframe using this page count list.
    df = build_dataframe(pages)
    #Display the page count frequencies as a histogram using the created dataframe.
    display_histogram(df)


main()