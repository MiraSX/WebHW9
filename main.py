from bs4 import BeautifulSoup
import requests
import json
from connect import connect
from models import Authors, Quotes

base_url = "https://quotes.toscrape.com"

html_doc = requests.get(base_url)
soup = BeautifulSoup(html_doc.text, "html.parser")
content = soup.select("div[class='quote']")
# print(content[0])

def load_json():
    links = []
    for el in content:
        quote = el.find("span", attrs={'class':"text"}).text
        author = el.find('small', attrs={"class":"author"}).text
        tags = [tag.text for tag in el.select('div[class="tags"] a')]
        link = links.append(el.find('a')['href'])
        quote = Quotes(tags=tags, author=author, quote=quote)
        quote.save()
    


    for link in links:
        html_doc = requests.get(base_url+link)
        soup = BeautifulSoup(html_doc.text, "html.parser")
        content2 = soup.select("div[class=author-details]")   
    
        for el in content2:
            fullname=el.find('h3').text
            born_date=el.find("p").find("span", attrs={"class":"author-born-date"}).text
            born_location=el.find("p").find("span", attrs={"class":"author-born-location"}).text
            description=el.find("div", attrs={"class":"author-description"}).text.strip()
                
            # print(fullname, born_date, born_location, description)
            author = Authors(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
            author.save()



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
    load_json()
