import time
import random
import json
import re
from bs4 import BeautifulSoup
from dateutil import parser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

import chromedriver_autoinstaller
chromedriver_autoinstaller.install() 


def start_selenium():
    """ This function will start an automated browser and first open wikipedia, then X. 
        Wait until the X page is fully loaded. Then, you can manually login to X,
        and answer the questions you are asked (e.g. solve a captcha or disable cookies
        when asked). Once you are finished and the X Newsfeed is fully visible, you can
        execute the next function, using this driver object.
        
        Alternatively, if you want to use another browser, you can use your own function to create a driver object.
        
        Caution: With this function, we try to simulate a normal Chrome browser, not a test browser. 
        To make this work, a Chrome browser needs to be installed on your system. If this functions 
        starts a browser in a test environment, check whether you have chrome installed.
        
        :returns: A driver object. This can be inserted in each function requiring the driver.
    """
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--profile-directory=Default")
    options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})
    driver = webdriver.Chrome(options=options)
    
    #Open Wikipedia, so that we have another start adress
    driver.get("https://en.wikipedia.org")
    time.sleep(random.randint(2,4))
    
    #Open X
    driver.get("https://x.com/home")
    return(driver)


def get_profile_details(driver, username):
    """
        Return profile metadata for a given user. This metadata includes for example the users statistics and biography. 
        More information on how a profile metadata object looks like can be found in the chapter source.
    
        :param str username: Provide username as string, eg. "xplodingunicorn". 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :returns: A profile metadata object (see source)
        :rtype: set
    """
    user_profile = {}
    
    driver.get('https://x.com/'+username)
    xpath_expression = '//*[@data-testid="UserProfileSchema-test"]'

    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath_expression)))

        json_str = element.get_attribute("innerText")
        profile = json.loads(json_str)
        
        author = profile.get('author', {})
        interaction_statistic = author.get('interactionStatistic', [])
        
        user_profile["given_name"] = author.get('givenName', None)
        user_profile["user_bio"] = author.get('description', None) if author.get('description') else None
        user_profile["user_location"] = author.get('homeLocation', {}).get('name', None) if author.get('homeLocation', {}).get('name') else None
        user_profile["number_of_followers"] = next((interaction['userInteractionCount'] for interaction in interaction_statistic if interaction['interactionType'] == 'https://schema.org/FollowAction'), None)
        user_profile["number_of_following"] = next((interaction['userInteractionCount'] for interaction in interaction_statistic if interaction['interactionType'] == 'https://schema.org/SubscribeAction'), None)
        user_profile["number_of_posts"] = next((interaction['userInteractionCount'] for interaction in interaction_statistic if interaction['interactionType'] == 'https://schema.org/WriteAction'), None)
        user_profile["user_website"] = profile.get("relatedLink", [])[0] if profile.get("relatedLink", []) else None
        user_profile["username"] = author.get('additionalName', None)
        user_join_date_str = profile.get('dateCreated', None)
        if user_join_date_str:
            user_join_date = parser.parse(user_join_date_str)
            user_profile["user_join_date"] = user_join_date.strftime('%d.%m.%Y')
        else:
            user_profile["user_join_date"] = None

        return user_profile

    except:
        print("Timed out waiting for elements to appear")
        return {}



def  get_followings_of_user(driver, username, n):
    """
        Return the names of users a given profile is following. 
        
        :param str username: Provide username as string, eg. "xplodingunicorn". 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int n: The number of followings, which should be collected. 
        :returns: A string list of usernames
        :rtype: list
    """
    driver.get('https://x.com/'+username+'/following')
    collected_usernames = []
    collected_elements = []
    xpath_expression = '//*[@data-testid="cellInnerDiv"]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span'
    while True:
        try:
            elements = WebDriverWait(driver, 1000).until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
           
            for element in elements:
                if len(collected_usernames) >= n:
                    break 
                if element not in collected_elements:
                    text = element.text.strip()
                    collected_elements.append(element)
                if text:
                    if text[1:] not in collected_usernames:
                        collected_usernames.append(text[1:])
                        
            if len(collected_usernames) >= n:
                break 

            #Check, whether end of page reached
            current_scroll_position = driver.execute_script("return window.scrollY")
            total_page_height = driver.execute_script("return document.body.scrollHeight")
            visible_window_height = driver.execute_script("return window.innerHeight")
            if current_scroll_position + visible_window_height >= total_page_height:
                print('End of page reached')
                break
            
            # Scroll down to load more followings
            scroll_duration=random.randint(1,2)
            end_time = time.time() + scroll_duration
            while time.time() < end_time:
                driver.find_element("xpath", "//body").send_keys(Keys.ARROW_DOWN)

            
        except Exception as e:
            continue 
    return collected_usernames
  

  
def get_followers_of_user(driver, username, n):
    """
        Return the names of users following a given profile. 
        
        :param str username: Provide username as string, eg. "xplodingunicorn". 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int n: The number of followers, which should be collected. 
        :returns: A string list of usernames
        :rtype: list
    """
    driver.get('https://x.com/'+username+'/followers')
    collected_usernames = []
    collected_elements = []
    xpath_expression = '//*[@data-testid="cellInnerDiv"]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span'
    while True:
        try:
            elements = WebDriverWait(driver, 1000).until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))
            initial_scroll_position = driver.execute_script("return window.scrollY;")
            for element in elements:
                if len(collected_usernames) >= n:
                    break 
                if element not in collected_elements:
                    text = element.text.strip()
                    collected_elements.append(element)
                if text:
                    if text[0] == '@' and text[1:] != username:
                        if text[1:] not in collected_usernames:
                            collected_usernames.append(text[1:])
                    
            if len(collected_usernames) >= n:
                break 

            #Check, whether end of page reached
            current_scroll_position = driver.execute_script("return window.scrollY")
            total_page_height = driver.execute_script("return document.body.scrollHeight")
            visible_window_height = driver.execute_script("return window.innerHeight")
            if current_scroll_position + visible_window_height >= total_page_height:
                print('End of page reached')
                break
            
            # Scroll down to load more followers
            scroll_duration=random.randint(1,2)
            end_time = time.time() + scroll_duration
            while time.time() < end_time:
                driver.find_element("xpath", "//body").send_keys(Keys.ARROW_DOWN)
                
        except Exception as e:
            continue 
    return collected_usernames


def get_tweets_of_user(driver, username, n):
    """
        Return the metadata of the tweets of a given user. The tweets contain all original tweets, replies, which
        are displayed on the post section on X and quotes (but not simple reposts without text).
        
        The metadata includes for example the tweets text.
        More information on how a tweet metadata object looks like can be found in the chapter source.
   
        :param str username: Provide username as string, eg. "xplodingunicorn". 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int n: The number of tweets, which should be collected. 
        :returns: A list of tweet objects (see source)
        :rtype: list
    """
    driver.get('https://x.com/'+username)
    username = username.lower()
    
    #Scroll to tweets
    driver.execute_script('window.scrollTo(0, 500)')
    time.sleep(random.randint(4, 6))

    tlinks=[]
    tcont={}

    while True:
        time.sleep(random.randint(3,5))
        
        #Collect the first 4-5 tweets
        tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')         
        #Save tweets of the user (ignore retweets und tweets of other users)
        for tweet in tweets:
            if (len(tlinks)>=n):
                break
            try: 
                tweetcontent = tweet.get_attribute('innerHTML').lower()
                tweetid = re.findall(username+"/status/([0-9]+)", tweetcontent)
                if (tweetid != []):
                    if (tweetid[0] not in tlinks):
                        tlinks.append(tweetid[0])
                        tcont[tweetid[0]]=tweetcontent
            except StaleElementReferenceException as e:
                nothingtodohere=0
        if (len(tlinks)>=n):
            break

        #Check, whether end of page reached
        current_scroll_position = driver.execute_script("return window.scrollY")
        total_page_height = driver.execute_script("return document.body.scrollHeight")
        visible_window_height = driver.execute_script("return window.innerHeight")
        if current_scroll_position + visible_window_height >= total_page_height:
            print('End of page reached')
            break
        
        # Scroll down to load more tweets
        scroll_duration=random.randint(1,2)
        end_time = time.time() + scroll_duration
        while time.time() < end_time:
            driver.find_element("xpath", "//body").send_keys(Keys.ARROW_DOWN)
        
    #Process Tweetcontent
    all_tweets = []
    
    for tweetid,tweet in tcont.items():
        try:
            tweetdata={}
            soup = BeautifulSoup(tweet, "html.parser")
            tweetdata['text'] = soup.find('div',attrs={"data-testid" : "tweettext"}).text
            tweetdata['username'] = soup.find('a')['href'].lstrip('/')
            tweetdata['link'] = 'https://x.com/'+tweetdata['username']+'/status/'+tweetid
            
            tweetdata['time'] = soup.find('time')['datetime']
            try: 
                statistics = soup.find('div',attrs={"role" : "group"})['aria-label']
                tweetdata['replies'] =  int([part.split()[0] for part in statistics.split(',') if 'repl' in part][0]) if 'repl' in statistics else 0
                tweetdata['reposts'] =  int([part.split()[0] for part in statistics.split(',') if 'repo' in part][0]) if 'repo' in statistics else 0
                tweetdata['likes'] =  int([part.split()[0] for part in statistics.split(',') if 'lik' in part][0]) if 'lik' in statistics else 0
                tweetdata['bookmarks'] =  int([part.split()[0] for part in statistics.split(',') if 'book' in part][0]) if 'book' in statistics else 0
                tweetdata['views'] =  int([part.split()[0] for part in statistics.split(',') if 'view' in part][0]) if 'view' in statistics else 0
            except:
                print('No statistics could be extracted for tweet', tweetid, '. This tweet might be an advertisement')
            finally:
                try: 
                    tweetdata['time'] = soup.find('time')['datetime']
                except:
                    print('No creation date could be extracted for tweet', tweetid, '. This tweet might be an advertisement')
                finally:
                    all_tweets.append(tweetdata) 
        except:
            print('Error with extracting data for tweet', tweetid)
            continue           
    return(all_tweets)



def get_tweets_by_keyword(driver, keyword, n):
    """
        Returns the metadata of the tweets for a given keyword or hashtag. This metadata includes for example the tweets text. 
        More information on how a tweet metadata object looks like can be found in the chapter source.

        :param str keyword: Provide a keyword, e.g. "funny dog" or hashtag, e.g. "#funny" as string. 
        :param selenium.WebDriver driver: The driver you have created with start_selenium() (or your own driver) 
        :param int n: The number of tweets, which should be collected. 
        :returns: A list of tweet objects (see source)
        :rtype: list
    """
    driver.get('https://x.com/home')
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 200)
    tlinks=[]
    tcont={}

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="off"]'))).send_keys(keyword)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    while True:
        time.sleep(random.randint(3,5))
        
        #Collect the first 4-5 tweets
        tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')         
        #Save tweets of the user (ignore retweets und tweets of other users)
        for tweet in tweets:
            if (len(tlinks)>=n):
                break
            try: 
                tweetcontent = tweet.get_attribute('innerHTML').lower()
                tweetid = re.findall("/status/([0-9]+)", tweetcontent)
                if (tweetid != []):
                    if (tweetid[0] not in tlinks):
                        tlinks.append(tweetid[0])
                        tcont[tweetid[0]]=tweetcontent
            except StaleElementReferenceException as e:
                nothingtodohere=0
        if (len(tlinks)>=n):
            break

        #Check, whether end of page reached
        current_scroll_position = driver.execute_script("return window.scrollY")
        total_page_height = driver.execute_script("return document.body.scrollHeight")
        visible_window_height = driver.execute_script("return window.innerHeight")
        if current_scroll_position + visible_window_height >= total_page_height:
            print('End of page reached')
            break
            
        # Scroll down to load more tweets
        scroll_duration=random.randint(1,2)
        end_time = time.time() + scroll_duration
        while time.time() < end_time:
            driver.find_element("xpath", "//body").send_keys(Keys.ARROW_DOWN)
        
    #Process Tweetcontent
    all_tweets = []
    
    for tweetid,tweet in tcont.items():
        try:
            tweetdata={}
            soup = BeautifulSoup(tweet, "html.parser")
            tweetdata['text'] = soup.find('div',attrs={"data-testid" : "tweettext"}).text
            tweetdata['username'] = soup.find('a')['href'].lstrip('/')
            tweetdata['link'] = 'https://x.com/'+tweetdata['username']+'/status/'+tweetid
            try: 
                statistics = soup.find('div',attrs={"role" : "group"})['aria-label']
                tweetdata['replies'] =  int([part.split()[0] for part in statistics.split(',') if 'repl' in part][0]) if 'repl' in statistics else 0
                tweetdata['reposts'] =  int([part.split()[0] for part in statistics.split(',') if 'repo' in part][0]) if 'repo' in statistics else 0
                tweetdata['likes'] =  int([part.split()[0] for part in statistics.split(',') if 'lik' in part][0]) if 'lik' in statistics else 0
                tweetdata['bookmarks'] =  int([part.split()[0] for part in statistics.split(',') if 'book' in part][0]) if 'book' in statistics else 0
                tweetdata['views'] =  int([part.split()[0] for part in statistics.split(',') if 'view' in part][0]) if 'view' in statistics else 0
            except:
                print('No statistics could be extracted for tweet', tweetid, '. This tweet might be an advertisement')
            finally:
                try: 
                    tweetdata['time'] = soup.find('time')['datetime']
                except:
                    print('No creation date could be extracted for tweet', tweetid, '. This tweet might be an advertisement')
                finally:
                    all_tweets.append(tweetdata)
        except:
            print('Error with extracting data for tweet', tweetid)
            continue           
    return(all_tweets)