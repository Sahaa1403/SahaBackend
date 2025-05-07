from django.db import models
from accounts.models import User
from datetime import datetime


class SearchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    text = models.CharField(max_length=10000)
    photo = models.ImageField(upload_to="Search_photo", null=True, blank=True)
    processed = models.BooleanField(default=False)
    cat_choices = (("real", "real"), ("fake", "fake"),)
    result = models.CharField(max_length=10, blank=True, null=True, choices=cat_choices)
    ai_answer = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text



class Label(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name


class Source(models.Model):
    title = models.CharField(max_length=90000)
    description = models.TextField(max_length=2000,null=True,blank=True)
    cat_choices = (("real", "real"), ("fake", "fake"),)
    category = models.CharField(max_length=10, blank=True, null=True, choices=cat_choices)
    default_label = models.ForeignKey(Label, on_delete=models.CASCADE, null=True,blank=True)
    photo = models.ImageField(upload_to="source_photo",null=True,blank=True)
    file = models.FileField(upload_to="source_file",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title



class SocialMedia(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(max_length=2000,null=True,blank=True)
    photo = models.ImageField(upload_to="socialmedia_photo",null=True,blank=True)
    file = models.FileField(upload_to="socialmedia_file",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title



class KnowledgeBase(models.Model):
    title = models.CharField(max_length=90000,blank=True,null=True)
    cat_choices = (("real","real"),("fake","fake"),)
    category = models.CharField(max_length=10,blank=True,null=True,choices=cat_choices)
    old_category = models.CharField(max_length=10,blank=True,null=True)
    body = models.TextField(max_length=90000,blank=False,null=True)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(Source,on_delete=models.CASCADE,null=True,blank=True)
    #label = models.ForeignKey(Label,on_delete=models.CASCADE,null=True,blank=True)
    keyword = models.CharField(max_length=2000,blank=True,null=True)
    location = models.CharField(max_length=2000,blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    photo = models.ImageField(upload_to="kb_photo", null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id) + ' | ' + str(self.category) + ' | ' + str(self.created_at)



class KnowledgeBaseLabelUser(models.Model):
    knowledge_base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('knowledge_base', 'user')  # One record per KB-user
    def __str__(self):
        return f"{self.knowledge_base.title} - {self.label.name}"
