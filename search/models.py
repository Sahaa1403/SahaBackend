from django.db import models
from mongoengine import Document, StringField, EmailField, DateTimeField, IntField
import datetime


class SearchData(Document):
    text = StringField(max_length=200)
    #email = EmailField(unique=True, required=True)
    #age = IntField()
    #created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'search'}  # Specify the collection name

