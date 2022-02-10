"""
Scrapes the GSoC archive of organizations from the years 2016 to 2021 using Selenium WebDriver.
Collects organizations names for each year, their GSoC links, and their logo urls.
"""
import json
import math

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_organizations(orgs: list, driver: WebDriver) -> None:
    """
    Get the organizations on each page.
    """
    orgs.extend(
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                ".grid__row.no-gap.ng-star-inserted div.grid__row__item"
            ))
        )
    )


def organize(data: dict, orgs: list, year: str, start: int = 0) -> None:
    """
    Organizes the data into a dictionary.
    """
    for org in orgs[start::]:
        # find the link of the current organization
        link = org.find_element(
            by=By.TAG_NAME,
            value="a"
        ).get_attribute("href")

        # find the name of the current organization
        name = org.find_element(by=By.CLASS_NAME, value="name").text

        # find the image url of the current organization
        img_url = org.find_element(
            by=By.TAG_NAME,
            value="img"
        ).get_attribute("src")

        # find the description of the current organization
        short_description = org.find_element(
            by=By.CLASS_NAME,
            value="short-description"
        ).text

        # save the data as a dictionary
        data[year].append(
            {
                name: {
                    "link": link,
                    "img_url": img_url,
                    "short_description": short_description
                }
            }
        )


def main() -> None:
    """
    The main method.
    """
    driver = webdriver.Chrome(service=Service("chromedriver.exe"))
    driver.maximize_window()

    # store all the organization details
    data = {"2009": [], "2010": [], "2011": [], "2012": [], "2013": [], "2014": [],
            "2015": [], "2016": [], "2017": [], "2018": [], "2019": [], "2020": [],
            "2021": []}

    for year in range(2016, 2022):
        # create new list of organizations for each year
        orgs = []

        # link to access the list of organizations for the current year
        driver.get(
            f"https://summerofcode.withgoogle.com/archive/{year}/organizations")

        # find number of orgs
        num_orgs = int(WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "div.mat-paginator-range-label"
            ))
        ).text.split()[-1])

        # organize the organization details
        get_organizations(orgs, driver)
        organize(data, orgs, str(year))

        # number of times to press next page button
        for i in range(math.ceil(num_orgs/50) - 1):

            # find the next page button
            button = driver.find_element(
                by=By.CSS_SELECTOR,
                value="button[aria-label='Next page']")

            # click the next page button using javascript
            driver.execute_script("arguments[0].click();", button)

            # organize the organization details
            get_organizations(orgs, driver)
            organize(data, orgs, str(year), start=50 + (i * 50))

    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    finally:
        driver.quit()


main()
