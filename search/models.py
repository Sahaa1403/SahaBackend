from django.db import models
from mongoengine import Document, StringField, EmailField, DateTimeField, IntField,  ReferenceField
import datetime


class SearchData(Document):
    text = StringField(max_length=200)
    #email = EmailField(unique=True, required=True)
    #age = IntField()
    #created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'SearchData'}  # Specify the collection name



class Label(Document):
    name = StringField(max_length=1000, required=True)

class KnowledgeBase(Document):
    title = StringField(max_length=1000)
    category = StringField(choices=["real", "fake"])
    old_category = StringField(max_length=10)
    body = StringField(max_length=5000, required=True)
    source = StringField(max_length=2000)
    label = ReferenceField(Label)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(KnowledgeBase, self).save(*args, **kwargs)




""" 
class Label(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name


class KnowledgeBase(models.Model):
    title = models.CharField(max_length=1000,blank=True,null=True)
    cat_choices = (("real","real"),("fake","fake"),)
    category = models.CharField(max_length=10,blank=True,null=True,choices=cat_choices)
    old_category = models.CharField(max_length=10,blank=True,null=True)
    body = models.TextField(max_length=5000,blank=False,null=True)
    source = models.CharField(max_length=2000,blank=True,null=True)
    label = models.ForeignKey(Label,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id + ' | ' + str(self.category) + ' | ' + str(self.created_at)
"""