# main_student.py

from myges_scrap_student import MyGesScrapStudent


def main():
    scraper = MyGesScrapStudent("username", "password")
    scraper.login()
    scraper.scrape_student()


if __name__ == "__main__":
    main()
