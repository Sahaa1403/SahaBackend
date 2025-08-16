from search.models import KnowledgeBaseLabelUser, KnowledgeBaseProcessStatus, Label
from search.models import KnowledgeBase
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

def create_kb_process_status(kbs: list[KnowledgeBase]):
    kb_process_status_list = [
        KnowledgeBaseProcessStatus(
                knowledge_base=kb,
        )

        for kb in kbs
    ]

    KnowledgeBaseProcessStatus.objects.bulk_create(kb_process_status_list, ignore_conflicts=True)
    print(f"{len(kb_process_status_list)} KBProcessStatus add to DB✅")

    