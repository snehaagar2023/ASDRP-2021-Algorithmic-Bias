from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.read_csv('yahoodata.csv')
top_stories_list = df['Headline'].tolist()
publication_list = df['Publication'].tolist()



for i in range(299):
    term = str(top_stories_list[i])
    term = term.replace(' ', '+')
    url = 'https://news.search.yahoo.com/search?q={}'.format(term)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='NewsArticle')
    if len(results) > 0:
        link = results[0].find('h4').a['href']
        i = 1
        while link.startswith("https://news.yahoo.com") == False and i < len(results):
            link = results[i].find('h4').a['href']
            i+=1
        print(link)
    else:
        print("ERROR")
