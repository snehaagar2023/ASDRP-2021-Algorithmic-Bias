import requests
import numpy
import pandas as pd
from bs4 import BeautifulSoup

key = 'gAAAAABeVpQJKRM5BqPX91XW2AKfz8pJosk182maAweJcm5ORAkkBFj__d2feG4H5KIeOKFyhUVSY_uGImiaSBCwy2L6nWxx4g=='

def getScore(transcript):
    if not transcript is None:
        try:
            return float(requests.post('https://api.thebipartisanpress.com/api/endpoints/beta/robert', data={'API':key,'Text':transcript}).text)
        except:
            print('request failed')
    return None

df = pd.read_csv("ynews.tsv", sep='\t')
df.insert(10, 'Bipartisan Press Bias', 'ERROR', False)
print(df)

response = requests.get('https://weather.com/');

for index, row in df.iterrows():
    s = ''
    print('Index: ' + str(index) + "\n")
    if row['Bipartisan Press Bias'] == 'ERROR':
        try:
            url = (row['Article'])
        except:
            continue
        if url != '':
            try:
                response = requests.get(url)
            except:
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.find_all("div", class_="caas-body-section")
            ptags = None
            try:
                ptags = divs[0].find_all('p')
            except:
                continue
            for i in ptags:
                s = s + i.get_text()

            score = getScore(s)
            print(s +'\n' + str(score) + '\n------------------------------')
            df.loc[index, 'Bipartisan Press Bias'] = score

            if (index%5 == 0 or index == len(df.index)-1):
                df.to_csv('ynews_e.csv',sep='\t',index=False) # Use Tab to seperate data
                print('exported\n')



# response = requests.get(url);
# s = ''
# soup = BeautifulSoup(response.content, 'html.parser')
# divs = soup.find_all("div", class_="caas-body-section")
# ptags = divs[0].find_all('p')
# for i in ptags:
#     print(i.get_text() + '\n\n')
