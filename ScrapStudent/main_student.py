# main_student.py

from myges_scrap_student import MyGesScrapStudent


def main():
    scraper = MyGesScrapStudent("aslimane1", "Hajar77176")
    scraper.login()
    scraper.scrape_student()


if __name__ == "__main__":
    main()
