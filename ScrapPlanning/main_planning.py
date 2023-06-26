# main_planning.py

from myges_scrap_planning import MyGesScrapPlanning


def main():
    scraper = MyGesScrapPlanning("username", "password")
    scraper.login()
    scraper.navigate_to_planning()
    scraper.scrape_planning()
    scraper.next_week()
    scraper.scrape_planning()
    scraper.close()


if __name__ == "__main__":
    main()
