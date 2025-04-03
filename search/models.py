from django.db import models
from mongoengine import Document, StringField, EmailField, DateTimeField, IntField
import datetime

class SearchData(Document):
    text = StringField(max_length=200)
    #email = EmailField(unique=True, required=True)
    #age = IntField()
    #created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'search'}  # Specify the collection name




class KnowledgeBase(models.Model):
    cat_choices = (("real","real"),("fake","fake"),)
    category = models.CharField(max_length=10, blank=True, null=True, choices=cat_choices)
    body = models.TextField(max_length=5000,blank=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id + ' | ' + str(self.category) + ' | ' + str(self.created_at)