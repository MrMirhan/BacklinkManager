from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from threading import Thread
from datetime import datetime
import os, logging, numpy
import Logger

Logger.logging.getLogger('WDM').setLevel(logging.WARNING)
logger = Logger.logging_start(True)
logging.getLogger('WDM').removeHandler(logging.WARNING)
Logger.logging.getLogger('WDM').removeHandler(logging.WARNING)

commentBox = ["comment", "comment_txt", "yorum"]
authorBox = ["author", "yazan"]
mailBox = ["email", "mail"]
urlBox = ["url"]
submitBox = ["submit", "gonder"]

def browserCreate():
    try:
        options = Options()
        args = [
                '--no-sandbox',
                '--log-level=0',
                '--disable-gpu',
                '--lang=tr',
                '--disable-dev-shm-usage',
                '--disable-browser-side-navigation',
                '--disable-setuid-sandbox',
                '--ignore-certificate-errors',
                '--headless'
            ]
        for arg in args:
            options.add_argument(arg)
        options.headless = True
        s=Service(ChromeDriverManager().install())    
        driver = webdriver.Chrome(service=s, options=options)
        driver.set_page_load_timeout(65)
        return driver
    except Exception as e:
        logger.error(e)
        return False

def find_elements(id, driver):
    for comment in commentBox:
        try:
            commentElement = driver.find_element(By.ID, comment)
            break
        except:
            try:
                commentElement = driver.find_element(By.NAME, comment)
                break
            except:
                logger.warning(f"Thread #{id} / Can't find comment area. Skipping..")
                return False
    for author in authorBox:
        try:
            authorElement = driver.find_element(By.ID, author)
            break
        except:
            try:
                authorElement = driver.find_element(By.NAME, author)
                break
            except:
                logger.warning(f"Thread #{id} / Can't find author area. Skipping..")
                return False
    for mail in mailBox:
        try:
            mailElement = driver.find_element(By.ID, mail)
            break
        except:
            try:
                mailElement = driver.find_element(By.NAME, mail)
                break
            except:
                logger.warning(f"Thread #{id} / Can't find mail area. Skipping..")
                return False
    for url in urlBox:
        try:
            urlElement = driver.find_element(By.ID, url)
            break
        except:
            try:
                urlElement = driver.find_element(By.NAME, url)
                break
            except:
                logger.warning(f"Thread #{id} / Can't find url area. Skipping..")
                return False
    for submit in submitBox:
        try:
            submitElement = driver.find_element(By.ID, submit)
            break
        except:
            try:
                submitElement = driver.find_element(By.NAME, submit)
                break
            except:
                logger.warning(f"Thread #{id} / Can't find submit area. Skipping..")
                return False
    return [commentElement, authorElement, mailElement, urlElement, submitElement]

def send_comment(id, commentElement, authorElement, mailElement, urlElement, submitElement):
    try:
        commentElement.send_keys("Harika bir yazı olmuş..")
        authorElement.send_keys("Alihan Cezmi")
        mailElement.send_keys("alihancezmi1@gmail.com")
        urlElement.send_keys("https://google.com")
    except:
        logger.error(f"Thread #{id} / While filling form an error occured. Skipping..")
        return False
    try:
        submitElement.click()
    except:
        logger.error(f"Thread #{id} / While submitting form an error occured. Skipping..")
        return False
    return True

def add_blacklist(url):
    with open("./blacklist.txt","a") as f:
        if url in blacklist:
            pass
        else:
            f.write('\n'+url)
        f.close()
        
def start_thread(id, backlinklist, create):
    logger.info(f'Thread #{id} - Successfully started for write {create} comments with {len(backlinklist)} length list.')
    driver = browserCreate()
    if not driver == False:
        created = 0
        thread_started = round(datetime.now().timestamp())
        for url in backlinklist:
            url_started = round(datetime.now().timestamp())
            if created == create:
                thread_finished = round(datetime.now().timestamp())
                logger.info(f"Thread #{id} / Finished with {created} comments in {thread_finished-thread_started} seconds. Average seconds per successfully comment was {round(((thread_finished-thread_started)/created), 2)}..")
                driver.quit()
                break
            try:
                driver.get(url)
                elems = find_elements(id, driver)
                if elems == False:
                    add_blacklist(url)
                    continue
                comment_sent = send_comment(id, elems[0], elems[1], elems[2], elems[3], elems[4])
                if comment_sent == False:
                    add_blacklist(url)
                    continue
                url_finished = round(datetime.now().timestamp())
                created+=1
                logger.info(f"Thread #{id} / T: {create} | C: {created} | L: {create-created} - Comment successfully in {url_finished-url_started} seconds added..")
                continue
            except TimeoutException as te:
                logger.warning(f"Thread #{id} / Timeout..")
                continue
            except AttributeError as ae:
                logger.error(f"Thread #{id} / No internet connection.. Quitting...")
                break
            except WebDriverException as wde:
                if wde.msg == " unknown error: net::ERR_INTERNET_DISCONNECTED":
                    logger.error(f"Thread #{id} / No internet connection.. Quitting...")
                    driver.quit()
                    break
                elif wde.msg == " disconnected: Unable to receive message from renderer":
                    logger.error(f"Thread #{id} / No internet connection.. Quitting...")
                    driver.quit()
                    break
                elif wde.msg == " unknown error: net::ERR_NAME_NOT_RESOLVED":
                    logger.error(f"Thread #{id} / Name not resolved..")
                    continue
                else:
                    logger.warning(f'Thread #{id} / Exception: ' + wde.msg)
                    continue
    else:
        logger.error(f"Thread #{id} / An error occured while creating web driver..")
blacklist = [url.replace('\n', '') for url in open('./blacklist.txt', 'r').readlines()]
urllist = [url.replace('\n', '') for url in open('./urllist.txt', 'r').readlines() if url.replace('\n', '') not in blacklist]
newlist = []
try:
    for x in [len(urllist), len(urllist)-1, len(urllist)-2]:
        if len(newlist) > 0: break
        for z in [5,4,3,2]:
            if x % z == 0:
                newlist = [list(x) for x in numpy.array_split(urllist[:x], z)]
                if not x == len(urllist):
                    indx = int(int(len(urllist)-x)*(-1))
                    newlist[len(newlist)-1] += urllist[indx:]
                logger.info(f'New list created for count of {len(newlist)} threads..')
                break
except Exception as exc:
    logger.error(exc)

if len(newlist) == 0:
    logger.error('New list could not created..')
    exit()

if __name__ == "__main__":
    try:
        total = int(input('How many backlinks do you want to add: '))
    except:
        logger.error("Please give an integer")
        exit()
    tocreate = []
    for x in [total, total-1,total-2,total-3,total-4]:
        exp = x % len(newlist)
        if exp==0:
            for y in newlist:
                tocreate.append(int(x/len(newlist)))
            if not x == total:
                tocreate[len(tocreate)-1] = tocreate[len(tocreate)-1] + total-x
            break
    thread_list = []
    a = 0
    for tlist in newlist:
        thread = Thread(target=start_thread, daemon=True, name=str(a), args=(a, tlist, tocreate[a]))
        thread_list.append(thread)
        a+=1
    for thread in thread_list:
        try:
            thread.start()
        except Exception as e:
            logger.error(f'While running thread #{newlist.index(tlist)} an error occured..')
    for thread in thread_list:
        try:
            thread.join()
            logger.info(f'Thread #{thread.getName()} - Thread finished..')
        except Exception as e:
            logger.error(e)
    input('Press any button to finish application..')