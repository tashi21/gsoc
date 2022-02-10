"""
Scrapes the GSoC archive of organizations from the years 2009 to 2015 using Selenium WebDriver.
Collects organizations names for each year, their GSoC links, and their logo urls.
"""
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main() -> None:
    """
    Main method.
    """
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    finally:
        driver = webdriver.Chrome(service=Service("chromedriver.exe"))
        driver.maximize_window()

    # select the year
    for year in range(2009, 2016):
        for org in data[str(year)]:
            for name in org:
                # link to access the organization's page
                driver.get(org[name]["link"])

                try:
                    # find the website of the organization
                    org[name]["website"] = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            "p a"
                        ))
                    ).get_attribute("href")

                except TimeoutException:
                    org[name]["website"] = None

    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    finally:
        driver.quit()


main()
