import csv
from bs4 import BeautifulSoup
import requests
import sqlite3
import time
from random import randint

path = "information.txt"
path2 = "Info.sqlite"
path3 = "information.csv"


def scrape_info():
    scraped_info = []
    page = 40

    while True:
        url = f"https://veli.store/category/tsignebi/mkhatvruli-literatura/tanamedrove/68/?page={page}"
        info = requests.get(url)
        soup = BeautifulSoup(info.text, 'html.parser')
        books = soup.find("div", class_="styled__ProductView-sc-183mmht-28 inZYkn")

        if not books:
            break

        all_books = books.find_all("div", class_="styled__CardWrapper-sc-1gjp82p-0 eknzBd")

        if not all_books:
            break

        for book in all_books:
            title = book.find("span", class_="title").text
            print(title)
            price_container = book.find("div", class_="prices")
            price_tag = price_container.find("span", class_="price").text
            print(price_tag)
            picture_container = book.find("a", class_="img-box").span.img.get("src")
            print(picture_container)
            print("------------------------------------------------------------------")

            scraped_info.append((title, price_tag, picture_container))

        page += 1
        time.sleep(randint(15, 20))

    return scraped_info


def save_into_csv(path_3, information):
    with open(path_3, 'w', encoding="utf-8_sig", newline='\n') as csvfile:
        f = csv.writer(csvfile, delimiter=',')
        for info in information:
            f.writerow([info[0], info[1], info[2]])


def save_into_file(path_1, information):
    with open(path_1, "w", encoding="utf-8") as file:
        for info in information:
            file.write(info[0] + " | " + info[1] + ' | ' + info[2] + "\n")

    file.close()


def save_into_database(path_2, information):
    conn = sqlite3.connect(path_2)
    curr = conn.cursor()
    curr.execute('''create table if not exists Main 
    (id integer primary key autoincrement,
    title text,
    price text,
    image text)''')
    for info in information:
        curr.execute('''insert into Main(title, price, image) values (?,?,?)''', (info[0], info[1], info[2]))

    conn.commit()
    conn.close()


def main():
    information = scrape_info()
    save_into_file(path, information)
    save_into_database(path2, information)
    save_into_csv(path3, information)


if __name__ == '__main__':
    main()
