import time
import warnings

import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

warnings.filterwarnings("ignore")


try:
    endRow = 3
    screenShotSize = (600, 338)

    NEWIMAGENAME = 'newimagename'
    WEBSITEURL = 'website_url'

    CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    CHROMEDRIVER_PATH = 'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # comment this line if you want to see the scraper working
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    driver2 = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)

    df = pd.read_csv('get-screenshots-from-url.csv', encoding='latin-1').drop(columns='name')

    for i in range(0, endRow+1, 2):
        driver.get(df[WEBSITEURL][i])
        driver2.get(df[WEBSITEURL][i+1])
        time.sleep(0.5)
        driver.get_screenshot_as_file(df[NEWIMAGENAME][i])
        driver2.get_screenshot_as_file(df[NEWIMAGENAME][i+1])

        image = Image.open(df[NEWIMAGENAME][i])
        region = image.resize(screenShotSize)
        region.save(df[NEWIMAGENAME][i], 'PNG', optimize=True, quality=100)

        image = Image.open(df[NEWIMAGENAME][i+1])
        region = image.resize(screenShotSize)
        region.save(df[NEWIMAGENAME][i+1], 'PNG', optimize=True, quality=100)

        print("Saved", df[NEWIMAGENAME][i])
        print("Saved", df[NEWIMAGENAME][i+1])

finally:
    driver.close()
    driver2.close()
    print("Done")
