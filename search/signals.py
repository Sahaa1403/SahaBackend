from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import KnowledgeBase, Label, KnowledgeBaseLabelUser, User

@receiver(post_save, sender=KnowledgeBase)
def assign_default_label(sender, instance, created, **kwargs):
    if not created:
        return  # فقط برای رکوردهای جدید اجرا میشه

    try:
        # گرفتن یا ساختن یوزر سیستمی
        
        system_user, _  = User.objects.get_or_create(
            email="system_user@yourapp.com",
            defaults={"username": "system_user", "name": "System User", "password": "system_user"}
        )


        # گرفتن یا ساختن لیبل "حقیقت"
        label, _ = Label.objects.get_or_create(name="حقیقت")

        # بررسی اینکه قبلاً این لیبل به این رکورد داده نشده باشه
        exists = KnowledgeBaseLabelUser.objects.filter(
            knowledge_base=instance,
            label=label,
            user=system_user
        ).exists()

        if not exists:
            KnowledgeBaseLabelUser.objects.create(
                knowledge_base=instance,
                label=label,
                user=system_user
            )
    except Exception as e:
        print("خطا در سیگنال:", e)