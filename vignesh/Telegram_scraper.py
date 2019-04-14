from requests import get
from bs4 import BeautifulSoup 
import csv
import pandas as pd
def clean(text):
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    return text
with open('telegraph_AA_INDIA_data.csv', 'w') as file:  # To delete the file content initially   
    writer = csv.writer(file)
    row = ['Heading', 'Publisher', 'Date', 'Body']
    writer.writerow(row)

rows = []
Url = 'https://www.telegraphindia.com/search/alcoholics-anonymous?page='
for pages in range(1,11):
    url = Url + str(pages) # retrived all 10 pages
    response = get(url)
    response = BeautifulSoup(response.text, 'html.parser')
    content = response.find('ul', class_='listing-withImage').find_all('li')
    try:
        for New_url in content:
            new_url = 'https://www.telegraphindia.com' + New_url.find('a')['href']
            new_response = get(new_url)
            new_response = BeautifulSoup(new_response.text, 'html.parser')
            new_content = new_response.find_all('div', class_='mainStory-normal')
            heading = new_content[0].find('h1').text
            publisher = new_content[0].find('div', class_='author-name').text
            date = new_content[0].find('ul', class_='rowUl').text.replace('Published', '').split('.')
            date[-1] = '20'+date[-1]
            date = '/'.join(date)
            body = ''
            body_text = new_content[0].find('div', style='margin: 10px 0').find_all('p')
            for b in body_text:
                body += clean(b.text)
            rows.append(heading)
            rows.append(publisher)
            rows.append(date)
            rows.append(body)
            with open('telegraph_AA_INDIA_data.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(rows)
                rows = []
                file.close()  
    except:
        pass
            
