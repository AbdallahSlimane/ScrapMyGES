import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyGesScrapMarks:
    def __init__(self, identifier, password):
        self.driver = webdriver.Chrome()
        self.identifier = identifier
        self.password = password

    def login(self):
        self.driver.get("https://myges.fr/login")
        time.sleep(2)
        identifier_box = self.driver.find_element(By.ID, "username")
        identifier_box.send_keys(self.identifier)
        password_box = self.driver.find_element(By.ID, "password")
        password_box.send_keys(self.password)
        password_box.send_keys(Keys.RETURN)
        time.sleep(2)

    def scrape_marks(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "marksForm:marksWidget:coursesTable_head"))
        )

        header_row = self.driver.find_element(By.ID, "marksForm:marksWidget:coursesTable_head")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        header_text = [cell.text for cell in header_cells]

        body_row = self.driver.find_element(By.ID, "marksForm:marksWidget:coursesTable_data")
        rows = body_row.find_elements(By.TAG_NAME, "tr")
        body_text = []

        for row in rows:
            marks_details = row.find_elements(By.TAG_NAME, "td")
            row_data = [detail.text for detail in marks_details]
            row_dict = {header_text[i]: value for i, value in enumerate(row_data)}
            body_text.append(row_dict)

        data = {
            "body": body_text,
        }

        return data

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

    def scrape_and_save_marks_for_specific_semesters(self):
        self.driver.get("https://myges.fr/student/marks")
        time.sleep(2)

        self.change_semester("2022-2023 - ESGI - 3ESGI  - Semestre 1")
        marks_semester_1 = self.scrape_marks()
        with open(f'marks_semester_1.json', 'w', encoding='utf-8') as f:
            json.dump(marks_semester_1, f, indent=4, ensure_ascii=False)

        self.change_semester("2022-2023 - ESGI - 3ESGI  - Semestre 2")
        marks_semester_2 = self.scrape_marks()
        with open(f'marks_semester_2.json', 'w', encoding='utf-8') as f:
            json.dump(marks_semester_2, f, indent=4, ensure_ascii=False)

        print("Data saved to marks_semester_1.json and marks_semester_2.json")

    def close(self):
        self.driver.quit()
