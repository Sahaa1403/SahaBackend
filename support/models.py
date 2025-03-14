from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField


class Ticket(models.Model):
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=False,null=True)
    answer = RichTextField(blank=False, null=True)
    satisfaction = models.IntegerField(default=0)
    image = models.ImageField(upload_to="ticket_image", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' | ' + str(self.created_date)
