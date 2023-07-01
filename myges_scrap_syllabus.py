import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class MyGesScrapSyllabus:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def change_semester(self, semester_label):
        dropdown_trigger = self.driver.find_element(By.CSS_SELECTOR, ".ui-selectonemenu-trigger")
        dropdown_trigger.click()
        time.sleep(5)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".ui-selectonemenu-item"))
        )
        dropdown_items = self.driver.find_elements(By.CSS_SELECTOR, ".ui-selectonemenu-item")
        for item in dropdown_items:
            if item.get_attribute("data-label") == semester_label:
                item.click()
                break
        time.sleep(5)

    def scrape_syllabus(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "coursesSyllabusForm:syllabusWidget:syllabusTable_head"))
        )
        header_row = self.driver.find_element(By.ID, "coursesSyllabusForm:syllabusWidget:syllabusTable_head")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        header_text = [cell.text for cell in header_cells]

        body_row = self.driver.find_element(By.ID, "coursesSyllabusForm:syllabusWidget:syllabusTable_data")
        rows = body_row.find_elements(By.TAG_NAME, "tr")

        body_text = []
        for row in rows:
            syllabus_details = row.find_elements(By.TAG_NAME, "td")
            row_data = [detail.text for detail in syllabus_details if detail.text and detail.text != 'ui-button']
            row_dict = {header_text[i]: value for i, value in enumerate(row_data)}
            body_text.append(row_dict)

        data = {
            "body": body_text,
        }
        return data

    def scrape_and_save_syllabus_for_specific_semesters(self, path, path_2):
        self.driver.get("https://myges.fr/student/syllabus-list")
        time.sleep(2)

        self.change_semester("2022-2023 - ESGI - 3ESGI  - Semestre 1")
        syllabus_semester_1 = self.scrape_syllabus()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(syllabus_semester_1, f, indent=4, ensure_ascii=False)

        self.change_semester("2022-2023 - ESGI - 3ESGI  - Semestre 2")
        syllabus_semester_2 = self.scrape_syllabus()
        with open(path_2, 'w', encoding='utf-8') as f:
            json.dump(syllabus_semester_2, f, indent=4, ensure_ascii=False)

    def close(self):
        self.driver.close()
