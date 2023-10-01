from mongoengine import Document
from mongoengine.fields import ListField, ReferenceField, StringField


class Authors(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=True)
    quote = StringField()