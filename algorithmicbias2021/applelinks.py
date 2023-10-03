import bs4
import requests

import pandas as pd

df = pd.read_csv('appledata.csv')
top_stories_list = df['Top Stories'].tolist()
publication_list = df['Publication'].tolist()

for i in range (299):
    query = str(top_stories_list[i]) + " " + str(publication_list[i])
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup =bs4.BeautifulSoup(resp.text,"html.parser")

    heading_object = soup.find_all('a')
    for i in range(len(heading_object)):
            if heading_object[i].get('href') == '/preferences':
                if(str(heading_object[i+1].get('href')).startswith("/")):
                    print(heading_object[i + 3].get('href'))
                else:
                    print(heading_object[i + 1].get('href'))