from django.db import models
from accounts.models import User

class SearchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    text = models.CharField(max_length=1000)
    ai_answer = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text


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
    keyword = models.CharField(max_length=2000,blank=True,null=True)
    location = models.CharField(max_length=2000,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id + ' | ' + str(self.category) + ' | ' + str(self.created_at)