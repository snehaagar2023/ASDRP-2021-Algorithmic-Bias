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

df = pd.read_csv("anews_e.csv", sep='\t')

#df.insert(10, 'Bipartisan Press Bias', 'ERROR', False)
print(df)

response = requests.get('https://weather.com/');

for index, row in df.iterrows():
    print('Index: ' + str(index) + "\n")
    if row['Bipartisan Press Bias'] == 'ERROR':
        url = (row['Article'])
        if url != '':
            try:
                response = requests.get(url)
            except:
                continue;
            soup = BeautifulSoup(response.content, 'html.parser')
            ptags = soup.find_all('p')
            s = ''
            if row['Publication'] == 'CNN':
                ptags = soup.find_all('div', class_='zn-body__paragraph')

            for i in ptags:
                # print(i.get_text())
                if('Yahoo' in row['Publication']):
                    inp = input('----------------------------\n' + i.get_text() + "\n\n" + row['Headline'] + " ---  (Yahoo)Is this ok?")
                    if inp == '1':
                        s = s + i.get_text()
                    elif inp == '3':
                        break
                elif(len(i.get_text()) > 40):
                    s = s + i.get_text()
                # elif(len(i.get_text()) > 30):
                #     inp = input('----------------------------\n' + i.get_text() + "\n\n Is this ok?")
                #     if inp == '1':
                #         s = s + i.get_text()
                else:
                    pass

            if(("500. That’s an error" in s ) or ("The page you requested was not found" in s)):
                # ok = input('----------------------------\n' + s + '\n\n Is the link broken?')
                # if ok == '1':
                df.loc[index, 'Bipartisan Press Bias'] = 'BADLINK'
                print('----------------------------\n' + 'BADLINK' + "\n\n")
                # else:
                #     score = getScore(s)
                #     print('----------------------------\n' + s + "\n\n")
                #     print('----------------------------\n' + str(score) + "\n\n")
                #     df.loc[index, 'Bipartisan Press Bias'] = score
            elif(('cookies and data gathered from your use of our platforms' in s) or ("To continue, please click the box below to let us know you're not a robot" in s)):
                # ok = input('----------------------------\n' + s + '\n\n Is the link a consent form?')
                # if ok == '1':
                df.loc[index, 'Bipartisan Press Bias'] = 'CONSENT'
                print('----------------------------\n' + 'CONSENT' + "\n\n")
                # else:
                #     score = getScore(s)
                #     print('----------------------------\n' + s + "\n\n")
                #     print('----------------------------\n' + str(score) + "\n\n")
                #     df.loc[index, 'Bipartisan Press Bias'] = score
            elif(len(s) > 33):
                score = getScore(s)
                print('----------------------------\n' + s + "\n\n")
                print('----------------------------\n' + str(score) + "\n\n")
                df.loc[index, 'Bipartisan Press Bias'] = score
            else:
                df.loc[index, 'Bipartisan Press Bias'] = 'LOWDATA'

        if (index%5 == 0 or index == len(df.index)-1):
            df.to_csv('anews_e.csv',sep='\t',index=False) # Use Tab to seperate data
            print('exported\n')

df.head()


# url='https://news.google.com/articles/CAIiENenQJBOgAusE-W_B2tdKEYqLQgEKiUIACIbd3d3LmJ1c2luZXNzaW5zaWRlci5jb20vc2FpKgQICjAMMJD-CQ?hl=en-US&amp;gl=US&amp;ceid=US:en&gl=US&ceid=US:en'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
# ptags = soup.find_all('p')
# s = ''
# for i in ptags:
#     # print(i.get_text())
#     if(len(i.get_text()) > 50):
#         s = s + i.get_text()
#     else:
#         inp = input(i.get_text() + "\n\n Is this ok?")
#         if inp == 1:
#             s = s + i.get_text()
#
# print(s)



# statement = '''Ex-President Donald Trump's big lie came full circle on Saturday as he traveled to Arizona to dangerously seize on the false fruits of a sham election "audit" precipitated by his own discredited claims the 2020 election was stolen.
#
# On a late afternoon of delusion and incitement, Trump offered a preview of how he could exploit grievances of millions of supporters who buy his lies about voter fraud to power a possible new presidential run in the future.
# His speech underscored the nation's split reality over last November's election — the real one in which he lost and President Joe Biden was fairly elected and the nonsensical but powerful one that he sells to his supporters.
# The now self-sustaining myth that Trump was improperly ejected from power is at the center of a belief system that the ex-President is imposing on his party and is making a litmus test for 2022 GOP candidates seeking his endorsement, including in the Arizona Senate race, which is one of the GOP's top targets as they try to take back the Senate.
# '''

# print(getScore(statement))
