from search.models import KnowledgeBaseLabelUser, KnowledgeBaseProcessStatus, Label
from search.models import KnowledgeBase
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

def assign_default_labels_to_kbs(kbs: list[KnowledgeBase]):
    User = get_user_model()

    # گرفتن یا ساخت یوزر سیستمی
    system_user, _ = User.objects.get_or_create(
        email="system_user@yourapp.com",
        defaults={
            "username": "system_user",
            "name": "System User",
            "is_active": False,
            "password": make_password(get_random_string(12)),
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



def create_kb_process_status(kbs: list[KnowledgeBase]):
    kb_process_status_list = [
        KnowledgeBaseProcessStatus(
                knowledge_base=kb,
        )

        for kb in kbs
    ]

    KnowledgeBaseProcessStatus.objects.bulk_create(kb_process_status_list)
    print(f"{len(kb_process_status_list)} KBProcessStatus add to DB✅")