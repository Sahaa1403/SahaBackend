from datetime import datetime, timedelta
import requests
from celery import shared_task
from search.models import KnowledgeBase



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
    

from django.db.models import  Q
@shared_task(name='search.tasks.trigger_send_kbs')
def trigger_send_kbs():
    print("===> Task Triggered")
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    unprocessed_kbs = KnowledgeBase.objects.filter(Q(created_at__gte=yesterday) & Q(processed=False))[:2]
    for kb in unprocessed_kbs:
        send_kb_to_ai.delay(kb.id)