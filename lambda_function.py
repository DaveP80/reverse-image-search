from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import re
import random
import logging
from tempfile import mkdtemp


def has_single_match(s, p):
    matches = re.findall(p, s, re.IGNORECASE)
    return len(matches) == 1

def lambda_handler(event, context):

    selflag = False
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(options=options, service=service)
    image_list_info = []
    itererr = False
    for i,image_url in enumerate(event["image_urls"]):
        # Navigate to Google Images
        if itererr:
            driver = webdriver.Chrome(options=options, service=service)
            driver.get("https://www.google.com/")
            wait = WebDriverWait(driver, 5)
        else: 
            driver.get("https://www.google.com/")
            wait = WebDriverWait(driver, 5)
        try:
            search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Search by image']")))
            search_icon.click()

            elementa = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Paste image link']")))

            elementa.send_keys(image_url)
            elementa.send_keys(Keys.RETURN)

            time.sleep(random.uniform(1.5, 2.2))
            div_element = None
            div_element = driver.find_element(By.XPATH, "//div[text()='See exact matches']")
            if div_element:
                div_element.click()

                driver.implicitly_wait(random.randint(2,3))
                ul_element = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='All results list']")

                anchor_elements = ul_element.find_elements(By.TAG_NAME, "a")
                stor = {"linkedin": [], "facebook": [], "youtube": [], "other": [] }
                href_list = [anchor.get_attribute("href") for anchor in anchor_elements]
                if len(href_list)>0:
                    for hl in href_list:
                        if has_single_match(hl[:23], r'linkedin'):
                            stor["linkedin"].append(hl)
                        elif has_single_match(hl[:23], r'youtube'):
                            stor["youtube"].append(hl)
                        elif has_single_match(hl[:23], r'facebook'):
                            stor["facebook"].append(hl)
                        else: stor["other"].append(hl)
                    
                    image_list_info.append({"image_link": image_url, "media_links": stor})
            itererr = False

        except NoSuchElementException as nerr:
            logging.error(nerr)
            itererr = True
            selflag = True
        finally:
            if i == len(event["image_urls"]) - 1:
                if not itererr:
                    driver.quit()
# Close the browser
    if len(image_list_info)>0:
        if selflag:
            return {
                'statusCode': 200,
                'body': {"issues": "unfound images", "data": image_list_info}
            }
        else:
            return {
                'statusCode': 200,
                'body': image_list_info 
            }
    else:
        return {
            'statusCode': 400,
            'body': {"issues": "no found images"}
        }
