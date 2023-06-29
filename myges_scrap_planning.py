import json
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyGesScrapPlanning:
    start_planning = "07:00"

    def __init__(self):
        self.driver = webdriver.Chrome()

    def navigate_to_planning(self):
        self.driver.get("https://myges.fr/student/planning-calendar")
        time.sleep(2)

    def scrape_event_details(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-event-inner")))
            event_elements = self.driver.find_elements(By.CSS_SELECTOR, ".fc-event-inner")
        except TimeoutException:
            print("No events found")
            return []

        events = [[] for _ in range(7)]
        curr_index = -1
        last_left = 0.0
        for i, event in enumerate(event_elements):
            hour = event.find_element(By.CSS_SELECTOR, ".fc-event-time").text.replace('\n', ' ')
            title = event.find_element(By.CSS_SELECTOR, ".fc-event-title").text.replace('\n', ' ')

            elements = self.driver.find_elements(By.CSS_SELECTOR, ".fc-event")
            if i >= len(elements):
                continue
            left = float(elements[i].value_of_css_property("left").replace("px", ""))

            if left != last_left:
                curr_index += 1
                last_left = left

            events[curr_index].append({
                "start_at": hour.split(" - ")[0],
                "end_at": hour.split(" - ")[1],
                "title": title.split("...")[0].strip(),
                "room": title.split("...")[1].strip()
            })

        for sublist in events:
            sublist.sort(key=lambda x: x["start_at"])
        return events

    def scrape_planning(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'calendar:currentWeek')))
        current_week_element = self.driver.find_element(By.ID, 'calendar:currentWeek')
        current_week_text = current_week_element.text.replace('\n', ' ')

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'calendar:lastUpdate')))
        last_update_element = self.driver.find_element(By.ID, 'calendar:lastUpdate')
        last_update_text = last_update_element.text.replace('\n', ' ')

        header_row = self.driver.find_element(By.CSS_SELECTOR, "table.fc-agenda-days thead tr")
        header_cells = header_row.find_elements(By.TAG_NAME, "th")
        header_text = [cell.text for cell in header_cells]

        events = self.scrape_event_details()

        data = {
            "week": current_week_text,
            "last_update": last_update_text,
            "day": header_text,
            "events": events,
        }

        with open('ScrapPlanning/planning.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Data saved to planning.json")
        return data

    def next_week(self):
        next_week_button = self.driver.find_element(By.ID, "calendar:nextMonth")
        next_week_button.click()
        time.sleep(5)

    def close(self):
        self.driver.quit()
