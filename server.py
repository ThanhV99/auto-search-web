from flask import Flask, request, render_template, jsonify

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        my_website = request.form['website']
        total_section = int(request.form['section'])
        max_page = int(request.form['max_page'])
        
        if my_website:
            print(my_website)

        
        for i in range(total_section):
            print(i)
            # Set up Chrome options (you can add more options as needed)
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--headless")  # Uncomment this line if you want headless mode
            # chrome_options.add_argument("--disable-gpu")  # Uncomment this line if needed
            # Create a WebDriver instance for Chrome with the specified options
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            # driver = webdriver.Chrome(options=chrome_options)
            # Navigate to the Google website
            driver.get("https://www.google.com/")
            time.sleep(1)  # Optional delay to allow the page to load

            # Perform your automation tasks here
            # For example, you can enter the keyword and website URL in Google's search box
            search_box = driver.find_element(By.ID, 'APjFqb')
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(3)

            # Close the browser when done
            driver.quit()
            
        return render_template('index.html', finish=True)

    return render_template('index.html', finish=False)


if __name__ == '__main__':
    app.run(debug=True)