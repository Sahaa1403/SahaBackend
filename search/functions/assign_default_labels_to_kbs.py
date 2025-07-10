from search.models import KnowledgeBaseLabelUser, Label
from search.models import KnowledgeBase
from django.contrib.auth import get_user_model

def assign_default_labels_to_kbs(kbs: list[KnowledgeBase]):
    User = get_user_model()

    # گرفتن یا ساخت یوزر سیستمی
    system_user, _ = User.objects.get_or_create(
        email="system_user@yourapp.com",
        defaults={
            "username": "system_user",
            "name": "System User",
            "is_active": False,
            "password": User.objects.make_random_password()
        }
    )

    # گرفتن یا ساخت لیبل حقیقت
    label, _ = Label.objects.get_or_create(name="حقیقت")
  
    kb_lable_user_list = [
        KnowledgeBaseLabelUser(
                knowledge_base=kb,
                label=label,
                user=system_user
        )

        for kb in kbs
    ]

    KnowledgeBaseLabelUser.objects.bulk_create(kb_lable_user_list, ignore_conflicts=True)
    print(f"{len(kb_lable_user_list)} KBLableUser add with default label to DB✅")