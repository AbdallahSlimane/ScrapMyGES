import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class MyGesScrapPlanning:
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

    def scrape_planning(self):
        self.driver.get("https://myges.fr/student/planning-calendar")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'calendar:currentWeek')))
        current_week_element = self.driver.find_element(By.ID, 'calendar:currentWeek')
        current_week_text = current_week_element.text.replace('\n', ' ')

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'calendar:lastUpdate')))
        last_update_element = self.driver.find_element(By.ID, 'calendar:lastUpdate')
        last_update_text = last_update_element.text.replace('\n', ' ')

        header_row = self.driver.find_element(By.CSS_SELECTOR, "table.fc-agenda-days thead tr")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        header_text = [cell.text for cell in header_cells]

        body_rows = self.driver.find_elements(By.CSS_SELECTOR, "table.fc-agenda-slots tbody tr")
        body_text = []
        for row in body_rows:
            time_cell = row.find_element(By.TAG_NAME, "th")
            time_text = time_cell.text
            body_text.append(time_text)

        data = {
            "Semaine Courante": current_week_text,
            "Dernière mise à jour": last_update_text,
            "Jour": header_text,
            "Heure": body_text,
        }

        print(data)

        with open('planning.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        time.sleep(5)

        print("Data saved to planning.json")
        time.sleep(5)

    def close(self):
        self.driver.quit()


