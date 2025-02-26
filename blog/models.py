from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from config.utils import unique_slug_generator


class PostComment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)



class Post(models.Model):
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,null=True,blank=True,unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=False,null=True)
    feedback_status = models.BooleanField(default=True)
    comment_status = models.BooleanField(default=True)
    comments = models.ManyToManyField(PostComment,blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)


