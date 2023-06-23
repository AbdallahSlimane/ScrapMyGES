# main_planning.py

from myges_scrap_planning import MyGesScrapPlanning


def main():
    scraper = MyGesScrapPlanning("aslimane1", "Hajar77176")
    scraper.login()
    scraper.scrape_planning()


if __name__ == "__main__":
    main()
