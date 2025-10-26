from django.db import models
from accounts.models import User
from datetime import datetime
from django.contrib.postgres.fields import ArrayField 

class SearchData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    text = models.CharField(max_length=10000)
    photo = models.ImageField(upload_to="Search_photo", null=True, blank=True)
    processed = models.BooleanField(default=False)
    cat_choices = (("real", "real"), ("fake", "fake"),)
    result = models.CharField(max_length=10, blank=True, null=True, choices=cat_choices)
    ai_answer = models.JSONField(null=True,blank=True)
    import_batch_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.text


class Label(models.Model):
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name

ORIGIN_TYPE_CHOICES = (
    ("domestic", "داخلی"),
    ("foreign", "خارجی"),
)
class Source(models.Model):
    title = models.CharField(max_length=90000)
    description = models.TextField(max_length=2000,null=True,blank=True)
    cat_choices = (
        ("real", "real"),
        ("fake", "fake"),
        ("حقیقت", "حقیقت"),
        ("نادرست", "نادرست"),
        ("فریب‌دهی", "فریب‌دهی"),
        ("مخرب", "مخرب")
    )
    def get_default_label():
        return Label.objects.get_or_create(name="حقیقت")[0].id
    category = models.CharField(max_length=10, blank=True, null=True, choices=cat_choices)
    origin_type = models.CharField(max_length=10, blank=True, null=True, choices=ORIGIN_TYPE_CHOICES)
    default_label = models.ForeignKey(Label, on_delete=models.CASCADE, null=True,blank=True, default=get_default_label)
    photo = models.ImageField(upload_to="source_photo",null=True,blank=True)
    file = models.FileField(upload_to="source_file",null=True,blank=True)
    source_uri = models.CharField(max_length=255, null=True,blank=True)
    source_data_type = models.CharField(max_length=255, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    


class SocialMedia(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(max_length=2000,null=True,blank=True)
    origin_type = models.CharField(max_length=10, blank=True, null=True, choices=ORIGIN_TYPE_CHOICES)
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
    body = models.TextField(max_length=90000)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(Source,on_delete=models.CASCADE,null=True,blank=True, related_name='knowledge_bases')
    #label = models.ForeignKey(Label,on_delete=models.CASCADE,null=True,blank=True)
    # default_label = models.ForeignKey(Label, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=2000,blank=True,null=True)
    location = models.CharField(max_length=2000,blank=True,null=True)
    url = models.URLField(max_length=5000, blank=True,null=True)
    photo = models.ImageField(upload_to="kb_photo", null=True, blank=True)
    image = models.URLField(max_length=5000, blank=True, null=True)
    processed = models.BooleanField(default=False)
    import_batch_id = models.UUIDField(null=True, blank=True)
    percentages = models.JSONField(null=True, blank=True, verbose_name="درصد هر لیبل", default=None)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_time_pub = models.DateTimeField(null=True, blank=True)
    uri = models.CharField(max_length=255, unique=True, null=True, blank=True)
    lang = models.CharField(max_length=50, blank=True,null=True)
    is_duplicate = models.BooleanField(blank=True,null=True)
    data_type = models.CharField(max_length=255, blank=True,null=True)
    is_news = models.BooleanField(null=True, blank=True)
    sim = models.FloatField(blank=True,null=True)
    sentiment = models.CharField(max_length=255, blank=True, null=True)
    wgt = models.BigIntegerField(blank=True, null=True)
    relevance = models.FloatField(blank=True, null=True)
    authors = ArrayField(models.CharField(max_length=255), null=True, blank=True)

    class Meta:
        indexes = [
        models.Index(fields=["processed"]),  # برای فیلتر سریع موارد پردازش‌شده/نشده
        models.Index(fields=["import_batch_id"]),  # برای ارتباط بین رکوردها در یک import
        models.Index(fields=["date_time_pub"]),  # برای کوئری‌های مبتنی بر زمان
        models.Index(fields=["social_media"]),  # برای فیلتر یا join سریع
        models.Index(fields=["source"]),  # برای join یا فیلتر
        models.Index(fields=["uri"]),
        # ایندکس‌های ترکیبی برای کوئری‌های ترکیبی:
        models.Index(fields=["social_media", "import_batch_id"]),
        models.Index(fields=["social_media", "import_batch_id", "processed"]),
        models.Index(fields=["processed", "import_batch_id"]),
        models.Index(fields=["created_at", "processed", "import_batch_id"]),
    ]

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
    

class KnowledgeBaseProcessStatus(models.Model):
    knowledge_base = models.OneToOneField(KnowledgeBase, on_delete=models.CASCADE, related_name='status')
    is_news_checking = models.BooleanField(default=False)
    is_news_check_failed = models.BooleanField(default=False)
    add_news_check_failed = models.BooleanField(default=False)
    add_news_checking = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['add_news_checking', 'add_news_check_failed']),
        ]