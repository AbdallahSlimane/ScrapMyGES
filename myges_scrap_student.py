import json
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class MyGesScrapStudent:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def scrape_student(self, path):
        self.driver.get("https://myges.fr/student/student-directory")
        time.sleep(5)

        rows = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//td[@class='ui-datagrid-column']")))

        data = []

        for row in rows:
            try:
                image_element = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//td[@class='mg_directory_container']/img")))
                image_url = image_element.get_attribute("src")
            except (NoSuchElementException, TimeoutException):
                image_url = None

            try:
                name_element = WebDriverWait(row, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//div[@class='mg_directory_text']")))
                name = name_element.text.replace('\n', ' ')
            except (NoSuchElementException, TimeoutException):
                name = None

            data.append({
                "name": name,
                "image_url": image_url,
            })

        print(data)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        time.sleep(5)

    def close(self):
        self.driver.quit()
