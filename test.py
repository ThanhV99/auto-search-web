from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def autoSearchWebsite(keyword, my_website, max_page):
    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    # option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options = option)
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
                    time.sleep(random.randint(10,15))
                    ########
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
        browser.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.randint(10,20))


def main():
    # Set up Chrome options for the proxy
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension('urban.crx')
    chrome_options.add_experimental_option('detach', True)

    # Create a Chrome WebDriver instance with proxy options
    driver = webdriver.Chrome(options=chrome_options)
    # Now, you can use the 'driver' instance with the desired fake IP to interact with websites
    # ...
    time.sleep(2)
    driver.get("chrome-extension://eppiocemhmnlbhjplcgkofciiegomcon/popup/index.html#/main")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/div/div/button[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/div/div/div[2]/div/div/div/button[2]").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/div/div/div[3]/div[2]/div/div[1]/input").click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,"/html/body/div/div/div[3]/div[2]/div/div[2]/div/ul/li[3]").click()
    time.sleep(15)
    
    
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://whatismyipaddress.com/")
    time.sleep(15)
    # Close the browser
    driver.quit()
    
    # print("-------------- Auto start -------------------")
    # keyword = 'Phan Công Khanh: “Trùm siêu xe” nổi cỡ nào? sssg-erp'
    # my_website = "https://sssg-erp.com"
    # max_page = 9
    # print(f"Search result in {max_page} pages")
    # print("---------Loop Start-----------------")
    # for i in range(30):
    #     print(f"Times: {i+1}")
    #     autoSearchWebsite(keyword, my_website, max_page=max_page)
    #     time.sleep(1)
    #     print("---------------------------")

if __name__ == "__main__":
    main()