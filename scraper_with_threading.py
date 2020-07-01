import threading
import time
import warnings

import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

warnings.filterwarnings("ignore")


def worker(driver, threadIndex):
    """thread worker function"""
    print('Driver Get rowNumberForThread[threadIndex] =', rowNumberForThread[threadIndex])
    driver.get(df[WEBSITEURL][rowNumberForThread[threadIndex]])
    time.sleep(0.5)
    driver.get_screenshot_as_file(df[NEWIMAGENAME][rowNumberForThread[threadIndex]])

    image = Image.open(df[NEWIMAGENAME][rowNumberForThread[threadIndex]])
    region = image.resize(screenShotSize)
    region.save(df[NEWIMAGENAME][rowNumberForThread[threadIndex]], 'PNG', optimize=True, quality=100)

    print("Saved", df[NEWIMAGENAME][rowNumberForThread[threadIndex]])
    return


try:
    nbrThreads = 3
    NEWIMAGENAME = 'newimagename'
    WEBSITEURL = 'website_url'
    screenShotSize = (600, 338)

    CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    CHROMEDRIVER_PATH = 'C:\Program Files (x86)\Google\Chrome\chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # comment this line if you want to see the scraper working
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.binary_location = CHROME_PATH

    drivers = []
    for i in range(0, nbrThreads):
        drivers.append(webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options))

    threads = []
    for i in range(0, nbrThreads):
        threads.append("NULL")

    df = pd.read_csv('get-screenshots-from-url.csv', encoding='latin-1').drop(columns='name')

    rowNumberForThread = [i for i in range(0, nbrThreads)]
    breakIndex = 9
    rowIndex = 0
    while True:
        for i2 in range(0, nbrThreads):
            if rowIndex > breakIndex:
                break
            rowNumberForThread[i2] = rowIndex
            threads[i2] = threading.Thread(target=worker, kwargs={"driver": drivers[i2], "threadIndex": i2})
            threads[i2].start()
            rowIndex = rowIndex + 1

        for thread in threads:
            thread.join()

        if rowIndex > breakIndex:
            break

finally:
    for driver in drivers:
        driver.close()
    print("Done")
