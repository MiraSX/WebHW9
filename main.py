import json
import argparse
import pathlib
import requests
from bs4 import BeautifulSoup

from connect import connect
from models import Authors, Quotes

base_url = "https://quotes.toscrape.com"

parser = argparse.ArgumentParser(description="Library")
parser.add_argument("--action", "--a")


def next_page():
    links = ['/']
    for l in links:
        html_doc = requests.get(base_url+l)
        soup = BeautifulSoup(html_doc.text, "html.parser")
        content = soup.select_one("div[class='col-md-8'] nav")
        try:
            next_link = content.find('li', attrs={'class':'next'}).find('a')['href']
            links.append(next_link)
        except AttributeError:
            continue
    return links


def create_jsons():
    result_quote = []
    result_autor = []

    for link in next_page():
        html_doc = requests.get(base_url+link)
        soup = BeautifulSoup(html_doc.text, "html.parser")
        content_quote = soup.select("div[class='quote']")

        for el in content_quote:

            quote = el.find("span", attrs={'class':"text"}).text
            author = el.find('small', attrs={"class":"author"}).text
            tags = [tag.text for tag in el.select('div[class="tags"] a')]

            result_quote.append({"quote":quote, "author":author, "tags":tags})

            link_to_bio = el.select_one("span a").get('href')

            html_doc_bio = requests.get(base_url+link_to_bio)
            soup_bio = BeautifulSoup(html_doc_bio.text, "html.parser")
            content_bio = soup_bio.select_one("div[class='author-details']")

            fullname= content_bio.find('h3').text
            born_date= content_bio.find("p").find("span", attrs={"class":"author-born-date"}).text
            born_location= content_bio.find("p").find("span", attrs={"class":"author-born-location"}).text
            description= content_bio.find("div", attrs={"class":"author-description"}).text.strip()

            result_autor.append({"fullname":fullname, "born_date":born_date, "born_location":born_location, "description":description})


    pathlib.Path("json").mkdir(parents=True, exist_ok=True)

    with open('json/quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(result_quote, fd, ensure_ascii=False,  indent=2)

    with open('json/authors.json', 'w', encoding='utf-8') as fd:
        json.dump(result_autor, fd, ensure_ascii=False,  indent=2)


        


def load_json():
    with open("json/authors.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for i in data:
            author = Authors(
                fullname=i["fullname"],
                born_date=i["born_date"],
                born_location=i["born_location"],
                description=i["description"],
            )
            author.save()

    with open("json/quotes.json", 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for i in data:
            authors = Authors.objects(fullname=i["author"]).first()
            try:
                c_id_a = authors.id
            except AttributeError:
                c_id_a = None

            quote = Quotes(tags=i["tags"], author=c_id_a, quote=i["quote"])
            quote.save()


def find():
    while True:
        command = input("Enter action: ")
        if command == "exit":
            break

        else:
            args = command.split(":")
            comm = args[0]

            if comm == "name":
                a = Authors.objects(fullname=args[1]).first()
                quotes = Quotes.objects(author=a.id)
                for quote in quotes:
                    print(quote.quote)

            if comm == "tag":
                quotes = Quotes.objects(tags=args[1])
                for quote in quotes:
                    print(quote.quote)

            if comm == "tags":
                for tag in args[1].split(","):
                    quotes = Quotes.objects(tags=tag)
                    for quote in quotes:
                        print(quote.quote)


if __name__ == "__main__":
    create_jsons()
    if parser.parse_args().action == "load":
        load_json()
    find()