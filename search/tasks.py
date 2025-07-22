from datetime import datetime, timedelta
import requests
from celery import shared_task
from search.models import KnowledgeBase, KnowledgeBaseLabelUser, Label
from accounts.models import User
from django.db.models import  Q


@shared_task(name='search.tasks.trigger_send_kbs')
def trigger_send_kbs():
    print("===> Task Triggered")
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    unprocessed_kbs = KnowledgeBase.objects.filter(Q(created_at__gte=yesterday) & Q(processed=False) & Q(import_batch_id__isnull=True))[:3]
    print("ssssssssssssssssss", unprocessed_kbs)
    for kb in unprocessed_kbs:
        send_kb_to_ai.delay(kb.id)

@shared_task(bind=True, name='search.tasks.send_kb_to_ai')
def send_kb_to_ai(self, kb_id):
    try:
        kb = KnowledgeBase.objects.get(id=kb_id)

        headers = {
            'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
            'Content-Type': 'application/json',
        }

        payload = {
            'category': kb.category,
            'id': str(kb.id),
            'body': kb.body,
        }

        response = requests.post('http://62.60.198.225:5682/text/kb/add_news',
                                    params=payload,
                                    headers=headers,
                                    timeout=(3, 30)  # ← 3 ثانیه برای اتصال، 60 ثانیه برای خواندن
                                    )
        if response.status_code == 200:
            kb.processed = True
            kb.save()
            print("✅ API sent for kb.id =", kb.id)
        else:
            print(f"❌ Failed to send kb {kb.id}")
            raise self.retry(exc=Exception(f"Status {response.status_code}"), countdown=30)
    
    except Exception as exc:
        raise self.retry(exc=exc,  countdown=30)
    

from django.utils.timezone import now, timedelta
from django.utils import timezone

@shared_task(name='search.tasks.trigger_process_unprocessed_batch')
def trigger_process_unprocessed_batch():
    today = now().date()
    # today = timezone.now().date()
    # یک batch_id پیدا کن که هنوز کامل نشده
    first_unprocessed = KnowledgeBase.objects.filter(
        processed=False, import_batch_id__isnull=False
    ).order_by('import_batch_id').values_list('import_batch_id', flat=True).first()

    print("ssssssssssss", first_unprocessed)
    if not first_unprocessed:
        print("===> unprocessed_batch not found")
        return
    process_news_batch.delay(str(first_unprocessed))


from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

@shared_task(name='search.tasks.process_news_batch')
def process_news_batch(batch_id):  
    print("===> Task Triggered")
    LABEL_MAPPING = {
        "real": "حقیقت",
        "mis": "نادرست",
        "dis": "فریب‌دهی",
        "mal": "مخرب",
    }
    kb_list = KnowledgeBase.objects.filter(processed=False, import_batch_id=batch_id)[:3]
    ai_client, _ = User.objects.get_or_create(
        email="ai_client@yourapp.com",
        defaults={
            "username": "ai_client",
            "name": "ai client",
            "is_active": False,
            "password": make_password(get_random_string(12)),

        }
    )

    for kb in kb_list:
        try:
            headers = {
                'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                'Content-Type': 'application/json',
            }
            payload = {'input_news': kb.body}
            response = requests.post(
                "http://62.60.198.225:5682/text/check_news",
                params=payload,
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print("✅ API sent for kb.id =", kb.id)
            else:
                print(f"❌ Failed to send kb {kb.id}")
                # raise self.retry(exc=Exception(f"Status {response.status_code}"), countdown=30)
            
        except Exception:
            continue  # اگه fail شد، این رکورد دفعه بعد دوباره بررسی میشه.

        percentages = data.get("percentages", {})
        if not percentages:
            continue
        
        max_label = max(percentages, key=percentages.get)
        label_title = LABEL_MAPPING.get(max_label)
        if not label_title:
            continue

        label = get_object_or_404(Label, name=label_title)
        with transaction.atomic():
            KnowledgeBaseLabelUser.objects.update_or_create(
                knowledge_base=kb,
                user=ai_client,
                defaults={'label': label}
            )
            kb.percentages = percentages
            kb.processed = True
            kb.save(update_fields=["percentages", "processed"])
