from newsplease import NewsPlease # An integrated web crawler and information extractor for news 
from bs4 import BeautifulSoup # Python library for pulling data out of HTML and XML files
from requests import get # standard for making HTTP requests in Python
import pandas as pd # library written for data manipulation and analysis
import sys #  System-specific parameters and functions

Title, Link = [], []

for index, i in enumerate(range(983)):    
    url = 'https://www.thehindu.com/search/?q=Alcoholics%20Anonymous&order=DESC&sort=publishdate&page=' + str(i)
    response = get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Extracts url's from Hindu about AA
    url = [soup.select('a.story-card75x1-text')[i]['href'] for i in range(len(soup.select('a.story-card75x1-text')))]
    Link.extend(url)
    
    # Extracts Headline's from Hindu about AA
    title = [soup.select('a.story-card75x1-text')[i].text.strip() for i in range(len(soup.select('a.story-card75x1-text')))]
    Title.extend(title)
    
    # Python's standard out is buffered
    sys.stdout.write('\r' + str(index))
    sys.stdout.flush()

headline, time, meeting, news, image, authors = [], [], [], [], [], []

for index, url in enumerate(Link):
    
    # Parse the url to NewsPlease 
    article = NewsPlease.from_url(url)
    
    # Extracts the Headlines of News Article related to AA
    try:
        headline.append(article.title)
    except:
        headline.append(None)
    
    # Extracts the Authors of News Article related to AA
    try:
        authors.append(article.authors)
    except:
        authors.append(None)
    
    # Extracts the Main_Image_url of News Article related to AA
    try:
        image.append(article.image_url)
    except:
        image.append(None)
    
    # Extracts the Published_Date of News Article related to AA
    try:
        time.append(str(article.date_publish))
    except: 
        time.append(None)
    
    # Extracts the AA meetings if available
    try:
        meeting.append(article.text.split('Alcoholics Anonymous:')[-1].strip())
    except:
        meeting.append(None)
      
    # Extracts the Main_News from Article related to AA
    try:
        news.append(article.text.strip())
    except:
        news.append(None)
        
    # Python's standard out is buffered
    sys.stdout.write('\r' + str(index) + ' : ' + str(url) + '\r')
    sys.stdout.flush()

tbl = pd.DataFrame({'Headline' : headline, 
                    'Authors' : authors, 
                    'Main_Image' : image, 
                    'Published_Date' : time, 
                    'Meetings' : meeting, 
                    'News' : news,
                    'Source_urls' : Link})

tbl.to_excel(input("Filename:  //include '.xls' at the end of the filename"))