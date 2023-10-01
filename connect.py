import configparser

from mongoengine import connect

config = configparser.ConfigParser()
config.read("config.ini")

user = config.get("DB", "user")
password = config.get("DB", "pass")
domain = config.get("DB", "domain")
dbname = config.get("DB", "dbname")


url = f"mongodb+srv://{user}:{password}@{domain}/{dbname}?retryWrites=true&w=majority"

connect(host=url, ssl=True)
