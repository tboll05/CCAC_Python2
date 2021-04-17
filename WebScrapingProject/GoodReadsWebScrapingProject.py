import random, requests
import pandas as pd
from bs4 import BeautifulSoup

#Generate URL with a randomly generated search ID
def create_URL():
    #Randomly generated number to act as the search ID for the URL.
    search_ID = str(random.randint(1,99999999))
    full_URL = "https://www.goodreads.com/book/show/" + search_ID
    return full_URL

#Request HTML code from GoodReads using the created URL.
def ping_website(url):
    #Send request to website.
    response = requests.get(url)
    #Use Beautiful Soup to parse out text of the HTML that is returned.
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

#Pull data from returned HTML code.
#Extract title of book.
def scrape_title(soup):
    #Find Book Title using property ID from HTML code.
    title = soup.find(property = "og:title")
    #Returns the title for a given book.
    return title["content"]

#Extract primary author of book.
def scrape_author(soup):
    #Find primary author using property ID from HTML code.  Returns first instance of books:author.
    author = soup.find(property = "books:author")
    #Split up returned text, isolating name of author.  Creates a list of the parts of the HTML code that are separated by a period.
    author = author["content"].split('.')
    #Author name will be last item in the newly created list.  Takes that last item and replaces the underscore with a space to properly format the Author name.
    author = author[len(author)-1].replace('_',' ')
    #Returns the primary author for a given book.
    return author

#Extract page count for the book.
def scrape_page_count(soup):
    #Find page count using property ID from HTML code.
    page_count = soup.find(property = "books:page_count")
    #Returns the page count for a given book.
    return page_count["content"]

def scrape_num_reviews(soup):
    #Find Number of Reviews using itemprop ID from HTML code.
    review_count = soup.find(itemprop = "reviewCount")
    #Returns the number of reviews for a given book.
    return review_count["content"]

# Scrape program - pings sites and scrapes data
def scrape():
    #Get user input on how many data points or books they want to get information from.
    total_scrapes = int(input("How many data points do you want to gather?"))
    #Create lists for storing scraped data.
    #titles = []
    #authors = []
    page_counts = []
    #Counter to track progress of scraping.
    counter = 1
    
    #Loop to scrape as many books as the user indicated.
    for i in range(total_scrapes):
        #Create an inital URL to ping website.
        full_URL = create_URL()
        #Use Beautiful Soup to get HTML code and parse it out.
        soup = ping_website(full_URL)

        #Try Except block to determine if page is valid.
        while True:
            try:
            #Try to extract a title from the current webpage.
                title = scrape_title(soup)
                break
            #If the webpage is not a valid book, there won't be HTML code with a property = "og:title" ID and you would get a TypeError.
            #If this happens, generate a new URL and keep trying until you get a webpage with a valid book.
            except TypeError:
                full_URL = create_URL()
                soup = ping_website(full_URL)
        
        #try:
        #    author = scrape_author(soup)
        #except TypeError:
        #    author = 'No Author'
        
        try:
        #Try to extract a page count from the current book.
            page_count = scrape_page_count(soup)
        #If book happens to not have page count listed, set it to 0.
        except TypeError:
            page_count = 0

        #titles.append(title)
        #authors.append(author)

        #Cast the page count number to an Integer and append it to a running list of scrape page count numbers.
        page_counts.append(int(page_count))
        
        #Scraping Progress Counter (This method allows you to overwrite the printout so you don't have a newline every pass)
        print(f"Pages scraped: {counter} of {total_scrapes}", end = '\r')
        counter += 1
    print()
    
    #Returns the list of compiled page counts.
    return page_counts

#Takes the list of page counts and creates a data frame out of it
def build_dataframe(list_page_counts):
    #Build a dictionary using the list of page counts you have compiled.
    data = {
        "Page Count" : list_page_counts
    }
    #Pass that dictionary to Pandas to create a DataFrame object.
    df = pd.DataFrame(data)
    #Return the data frame object.
    return df

#Display Page Counts Frequencies in a Histogram
def display_histogram(dataframe):
    #Pass in a data frame object and display it as a histogram.  Default bin count is 10.
    return df.hist()

def main():
    #Compile your page counts.
    pages = scrape()
    #Make a data frame out of them.
    df = build_dataframe(pages)
    #Display the data as a histogram.
    display_histogram(df)


main()