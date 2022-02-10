"""
Scrapes the GSoC archive of organizations from the years 2009 to 2015 using Selenium WebDriver.
Collects organizations names for each year, their GSoC links, and their logo urls.
"""
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def organize(data: dict, orgs: list, year: str) -> None:
    """
    Organizes the data.
    """
    for org in orgs:
        # find the anchor tag of the current organization
        anchor_tag = org.find_element(
            by=By.TAG_NAME,
            value="a"
        )

        try:
            # find the image url of the current organization
            img_url = org.find_element(
                by=By.TAG_NAME,
                value="img"
            ).get_attribute("src")

        except NoSuchElementException:
            img_url = None

        finally:
            # save the data as a dictionary
            data[year].append(
                {
                    anchor_tag.text: {
                        "link": anchor_tag.get_attribute("href"),
                        "img_url": img_url,
                        "short_description": None,
                        "tech_stack": None,
                        "topics": None
                    }
                }
            )


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
        # link to access a given year's page
        driver.get(f"https://www.google-melange.com/archive/gsoc/{year}")

        # find the organizations on the page
        orgs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                "span.mdl-list__item-primary-content"
            ))
        )
        organize(data, orgs, str(year))

    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    finally:
        driver.quit()


main()
