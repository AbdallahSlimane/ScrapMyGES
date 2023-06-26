# main_scrap_marks.py

from myges_scrap_marks import MyGesScrapMarks


def main():
    scraper = MyGesScrapMarks("username", "password")
    scraper.login()
    scraper.scrape_and_save_marks_for_specific_semesters()
    scraper.close()


if __name__ == "__main__":
    main()
