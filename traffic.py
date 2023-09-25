from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import random

import threading

def multi_directTraffic(my_website, number_traffics):
    threads = []
    for url, number_traffic in zip(my_website, number_traffics):
        thread = threading.Thread(target=directTraffic, args=(url, number_traffic))
        threads.append(thread)
        
    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        

def directTraffic(url, number_traffic):
    try:
        for i in range(number_traffic):
            try:
                browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                browser.get(url)
                time.sleep(5)
                scroll_down(browser)
                # Rest of your code
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                if 'browser' in locals():
                    browser.quit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def autoSearchWebsite(keyword, my_website, max_page):
    # option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    # option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get("https://www.google.com/")
    time.sleep(2)

    search_box = browser.find_element(By.ID, 'APjFqb')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    is_page = False

    time.sleep(5)

    try:
        for page_number in range(1,max_page):
            
            link_element = browser.find_element(By.XPATH, '//*[@id="rso"]')
            a_elements = link_element.find_elements(By.TAG_NAME, 'a')
            
            for i in a_elements:
                link_url = i.get_attribute("href")
                if my_website in link_url:
                    i.click()
                    is_page = True
                    
                    time.sleep(random.randint(7,10))
                    scroll_down(browser)
                    ########
                    browser.execute_script(f"window.scrollBy(0, -200);")
                    browser.find_element(By.XPATH, '//*[@id="comments"]/button').click()
                    time.sleep(random.randint(15,20))
                    ########
                    browser.find_element(By.XPATH, '//*[@id="main"]/section/div/div/article[1]/div/a').click()
                    time.sleep(random.randint(7,10))
                    scroll_down(browser)
                    #######
                    browser.find_element(By.XPATH, '//*[@id="main"]/section/div/div/article[1]/div/a').click()
                    time.sleep(random.randint(7,10))
                    scroll_down(browser)
                    time.sleep(random.randint(15,20))
                    
                    break

            if not is_page:
                next_page = browser.find_element(By.XPATH, '//*[@id="pnnext"]/span[2]') 
                next_page.click()
                page_number += 1
            else:
                break
            time.sleep(1)
    except Exception as e:
        print("Error occurred while waiting:", e)

    if is_page:
        print(f"Website find in page {page_number}")
    else:
        print(f"No website result in {page_number} page")
    time.sleep(2)

    browser.quit()


def scroll_down(browser):
    total_height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
    viewport_height = browser.execute_script("return Math.max(document.documentElement.clientHeight, window.innerHeight || 0);")
    num_scrolls = int(total_height / viewport_height)
    
    max_scroll = browser.execute_script("return window.innerHeight;")
    scroll_distance = random.randint(100, max_scroll)
    for i in range(num_scrolls):
        browser.execute_script(f"window.scrollBy(0, {max_scroll});")
        time.sleep(random.randint(20,25))


def main():
    print("-------------- Auto start -------------------")
    keyword = 'Apple Pay bắt đầu ra mắt tại Việt Nam'
    # my_website = 'https://sssg-erp.com'
    my_website = "https://sssg-erp.com/dai-gia-dieu-cay-le-thanh-than-duoc-diu-de-ra-toa/"
    max_page = 9
    print(f"Search result in {max_page} pages")
    print("---------Loop Start-----------------")
    for i in range(30):
        print(f"Times: {i+1}")
        autoSearchWebsite(keyword, my_website, max_page=max_page)
        # directTraffic(my_website)
        time.sleep(5)
        print("---------------------------")

if __name__ == "__main__":
    main()