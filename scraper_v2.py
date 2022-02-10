"""
Scrapes the GSoC archive of organizations from the years 2016 to 2021 using Selenium WebDriver.
Collects the tech stack, topics, and website of each organization for each year.
"""
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
    for year in range(2016, 2022):
        # select the organization
        for org in data[str(year)]:
            # edit the tech stacks and topics of the organization
            for name in org:
                # link to access the organization's page
                driver.get(org[name]["link"])

                # find the tech stack of the organization
                org[name]["tech_stack"] = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "div.tech__content"
                    ))
                ).text.split(", ")

                # find the topics of the organization
                org[name]["topics"] = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "div.topics__content"
                    ))
                ).text.split(", ")

                # find the website of the organization
                org[name]["website"] = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "a.link"
                    ))
                ).get_attribute("href")

    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    finally:
        driver.quit()


main()
