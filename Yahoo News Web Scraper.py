from bs4 import BeautifulSoup as btfs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import date
from threading import Thread
import threading
import ctypes
import pandas as pd
from multiprocessing import Process # won't work for our multithreading since memory is not shared
# (when starting a new process a new selenium instance is made that copies previous search history)
# pretty sure it's just selenium getting really confused (it also doesn't even run the function)



# helping functions
#########################################################################################

class thread_with_exception(threading.Thread):
    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    # raises an exception in the thread
    def terminate(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))

        print("terminated thread")

        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# there aren't comments for how I get certain pieces of information
# this is because where information is in the html is specific to certain cites
# the information is extracted specific to yahoo news and is self explanatory

def create_soup(browser):
    html = browser.page_source  # get html
    soup = btfs(html, 'html.parser')  # get soup
    return soup

# for href links that might not have the homepage at the beginning
# also returns the true link
def click_link(link):
    if link[:5] == 'https':
        browser.get(link)
        time.sleep(1)  # so that the browser doesn't start lagging and an exception for unkown state is thrown
        return link
    else:
        # browser.find_element_by_xpath(f'//a[@href="{link}"]').click()  # only works if browser is on homepage
        browser.get(homepage + link)
        time.sleep(1) # so that the browser doesn't start lagging and an exception for unkown state is thrown
        return homepage + link

def open_page(link):
    browser.get(link)

# sometimes get hangs when opening mediabiasfactcheck and the script just stops doing anything
# we keep trying to get the bias information until it works
threads = []
status = [] # stores a set for each process which contains the current checkpoints passed
completed_len = 3
return_value = []

# checks the status of the process and terminates if it appears to have froze/hung
def check_status(thread_num,t=30):
    time.sleep(t)
    if "opened mbfc" not in status[thread_num]:
        threads[thread_num].terminate()
        return

    time.sleep(t)
    if "searched mbfc" not in status[thread_num]:
        threads[thread_num].terminate()
        return

    time.sleep(t)
    if "found bias" not in status[thread_num]:
        threads[thread_num].terminate()
        return

def try_to_get_bias_of_publication(publication, thread_num):
    print("trying to get bias")
    # create Chrome webdriver instance
    option = webdriver.ChromeOptions()
    option.add_argument('incognito')  # opens in incognito
    option.add_argument('headless') # prevents selenium from opening webpage
    # option.add_argument('--disable-browser-side-navigation') # prevent hanging after calling get()?
    browser = webdriver.Chrome(r'C:\Users\elija\Desktop\CODING\Random\Web scraping\chromedriver (2)', options=option)
    browser.set_page_load_timeout(30)

    # get bias of article from extracting information from mediabiasfactcheck.com
    mbfc_slant = None

    # get_guaranteed("https://mediabiasfactcheck.com/?s=" + '+'.join(publication.split())) # search for publication
    browser.get("https://mediabiasfactcheck.com")
    status[thread_num].add("opened mbfc")
    time.sleep(1)

    # closing ad
    '''print("finding_x")
    try:
        x_to_close_ad = browser.find_element_by_xpath("//button [@class='hustle-button-icon hustle-button-close']")
        x_to_close_ad.click()  # have to close ad that pops up so that page source is accessible
        print("clicked x")
        time.sleep(1)
    except Exception:
        pass
    '''

    search_box = browser.find_element_by_class_name("search-field").send_keys(publication)
    search_box = browser.find_element_by_class_name("search-field").send_keys(Keys.ENTER)
    status[thread_num].add("searched mbfc")
    time.sleep(1)

    print("creating_soup for mbfc search")
    soup = create_soup(browser)
    print("soup created")

    if soup.find(
            text='Sorry, but nothing matched your search terms. Please try again with different keywords.') == None:
        print("found match for search result")
        # some results matched
        first_article = soup.find('article').div.a['href']
        browser.get(first_article)
        time.sleep(1)

        print("creating soup for mbfc first article")
        soup = create_soup(browser)
        print("soup created")

        # mbfc_slant = soup.find('h3', text="Detailed Report").find_next('p').span.strong.contents[0]
        # above sometimes gets something formatted wrong(html still there like <strong>) or "High"(scrapes factuality score)
        mbfc_slant = soup.find('span',{'style': 'text-decoration: underline;'}).contents[0]

    else:
        print("did not find match for search result")
        # no results matched
        mbfc_slant = "N/A"

    status[thread_num].add("found bias")
    browser.close()

    return_value[thread_num] = mbfc_slant

def get_bias_of_publication(publication, tries = 3):
    print("getting bias of publication")

    if publication in bias_data_mbfc.index:
        print("publication already in database")
        return bias_data_mbfc.loc[publication][0]

    print("finding from mbfc site")
    for i in range(tries):
        print(f"try number: {i+1}")
        print("status: ", status)
        thread_num = len(threads)

        # create thread that tries to get the bias
        try_to_get_bias = thread_with_exception(target = try_to_get_bias_of_publication, args =(publication,thread_num)) # make process
        threads.append(try_to_get_bias) # append for easy access for termination if needed
        try_to_get_bias.start() # try to open page
        status.append(set())
        return_value.append(None)

        # run check_status
        check = Thread(target=check_status, args=(thread_num,))
        check.start()

        # keep on waiting until page is loaded or page is terminated
        while threads[thread_num].is_alive():
            time.sleep(0.1)

        if len(status[thread_num]) == completed_len:
            # page was properly opened otherwise the process would have been forcefully terminated
            # by thread "check_status" and the 3 checkpoints would not have been passed

            if not isinstance(return_value[thread_num],str) or len(return_value[thread_num]) > 20:
                # did not scrape properly because either
                # 1. The return value is not a string (there are some nested tags)
                # 2. The return value is a string (no nested tags, but we got the wrong thing)
                return_value[thread_num] = 'N/A'

            bias_data_mbfc.loc[publication] = return_value[thread_num] # add to database
            print("added publication to database")

            return bias_data_mbfc.loc[publication][0]
    else:
        print(f"failed to get bias after {tries} attempts")
        return "Too many tries, Find Manually"


def up_to_href(curr):
    while 'href' not in curr.attrs:
        curr = curr.parent

    return curr

def down_to_href(curr):
    while 'href' not in curr.attrs:
        curr = curr.contents[0]

    return curr

def scroll_down(y, browser):
    browser.execute_script(f"window.scrollTo(0, {y})")
    time.sleep(1) # so that the browser doesn't start lagging and an exception for unkown state is thrown
# unfinished
def scroll_infinite(y):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


#########################################################################################



# main code
#########################################################################################

directory = r'C:\Users\elija\Desktop\CODING\ASDRP\ASDRP-2021-Summer'
headline_data = pd.DataFrame(columns = ['Yahoo News Headline', 'Link to Headline', 'Publication', 'MB/FC Slant',
                                        'Rank Number', 'Date Recorded', 'Within 24 Hours?'])

# index_col = 0 so it uses the first column as the index (otherwise auto appends 0...n-1)
# keep_default_na = False so that N/A is not parsed and read as a numpy.nan
bias_data_mbfc = pd.read_csv(directory + r'\Bias\MediaBiasFactCheck.csv',index_col=0,keep_default_na=False)


# create Chrome webdriver instance
option = webdriver.ChromeOptions()
option.add_argument('incognito') # opens in incognito
option.add_argument('headless') # prevents selenium from opening webpage
# option.add_argument('--disable-browser-side-navigation') # prevent hanging after calling get()?
browser = webdriver.Chrome(r'C:\Users\elija\Desktop\CODING\Random\Web scraping\chromedriver',options=option)
browser.set_page_load_timeout(30)

# use Chrome webdriver to open yahoo news homepage
homepage = 'https://news.yahoo.com/'
browser.get(homepage)
soup = create_soup(browser)


# get headlines (links to the articles about them)
headlines_to_get = 30

# get first 6? headlines at the very top of the site
first_headlines = [up_to_href(i)['href'] for i in soup.find_all('img', attrs = {'tabindex':"-1"})]

headlines_to_get -= len(first_headlines)

# get the next "normal" headlines listed more in a list (top down) manner
# website is dynamic and there might not be enough headlines at first,
# so keep scrolling down until we get the required number of headlines
amt_to_scroll = 2000
while headlines_to_get > 0:
    #print(len(browser.page_source))
    second_headlines = [down_to_href(i)['href'] for i in soup.find_all('h3', attrs = {'class':['Ov(h)', 'Mend(10px)--maw1024', 'Mb(5px)']}, limit = headlines_to_get)]

    if len(second_headlines) < headlines_to_get:
        #print(len(second_headlines))
        scroll_down(amt_to_scroll, browser)
        soup = create_soup(browser)
        amt_to_scroll *= 2
    else:
        second_headlines = second_headlines[:headlines_to_get]
        headlines_to_get = 0

headlines = first_headlines + second_headlines


today = date.today().strftime("%B %d, %Y") # date in textual month, day, year format
# today = 'July 27, 2021'
# get information from the article for each headline
for i, headline in enumerate(headlines, 1):
    headline = click_link(headline) # get link
    print('\n\n\t', "headline: ", headline)

    print("creating soup for headline")
    soup = create_soup(browser)
    print("created soup for headline")

    # extract information from article

    title = soup.find('h1').contents[0]
    print("title:", title)

    try:
        publication = soup.find('img',{'class' : 'caas-img caas-loaded'})['alt']
    except (AttributeError, TypeError) as e:
        print(e)
        publication = f"couldn't scrape, find manually here: {headline}"
    print("publication:", publication)

    rank_number = i
    print("rank_number:", rank_number)

    try:
        date = soup.find('time').contents[0]
        date = date[date.index(',')+2:] # removes the day of week and starts at month now
        same_day = date[:len(today)] == today
    except (AttributeError, TypeError) as e:
        print(e)
        same_day = f"couldn't scrape, find manually here: {headline}"
    print("same_day:", same_day)

    mbfc_slant = get_bias_of_publication(publication)
    print("mbfc_slant:", mbfc_slant)

    # add information for article to pandas DataFrame
    headline_data.loc[headline_data.shape[0]] = [title, headline, publication, mbfc_slant,
                                                 rank_number, today, same_day]

browser.close()
print("closed browser")

print('\n\n')

# writing headline data to a csv file
headline_data.to_csv(directory + r'\Yahoo News Headline Data\Yahoo News Headline Data ' + today + '.csv')
print("saved headline data to csv")

# writing bias data from mbfc to a csv file
bias_data_mbfc.to_csv(directory + r'\Bias\MediaBiasFactCheck.csv')
print("saved bias data to csv")
#########################################################################################



''' 
random junk that I'm not deleting because I might use it in the future 
'''

# turns out tabindex = -1 gets first 6, but saving this just in case something changes
# the next 5 headlines are formatted differently in small icons under the first large headline
# one_to_six = [i for i in soup.find_all('div',attrs={'class': 'Pos(r)'}) if len(i['class']) == 1][:5]
# print(len(one_to_six))
# print(*one_to_six,sep = '\n\n\n\n')

# below won't work since selenium webdriver is not thread safe
# (you can't use the same chrome driver instance in multiple threads)
# however it is fine to have

'''
# sometimes get hangs and the script just stops doing anything
# we keep trying to get the page until it stops timing out
threads = []
succeeded = []

def check_after_t(page,t=10):
    time.sleep(t)
    if threads[page].is_alive():
        threads[page].terminate()
        succeeded[page] = 0

def get_guaranteed(link, tries = 30):
    for i in range(tries):
        page = len(threads) - 1
        # checks if next process (opening page) has finished after t seconds
        check = Process(target=check_after_t, args=(page,))
        check.start()
        open_page_process = Process(target = open_page, args =(link)) # make process
        threads.append(open_page_process) # append for easy access for termination if needed
        open_page_process.start() # try to open page
        succeeded.append(1) # change to 0 if it fails

        # keep on waiting until page is loaded or page is terminated
        while threads[page].is_alive():
            time.sleep(0.1)

        if succeeded[page]:
            # page was properly opened otherwise the process would have been
            # forcefully terminated by process "check" and succeeded[page] = 0
            break
    else:
        print(f"failed to properly load page after {tries} attempts")
        raise Exception
'''