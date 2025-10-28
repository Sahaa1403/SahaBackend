from datetime import datetime, timedelta
import requests
from celery import shared_task
from search.functions.public_functions import build_chart_data, call_check_news_api, get_ai_client, save_search_item, update_labels
from search.models import KnowledgeBase, KnowledgeBaseLabelUser, KnowledgeBaseProcessStatus, Label
from accounts.models import User
from django.db.models import  Q
from django.db import transaction

@shared_task(name='search.tasks.trigger_send_kbs')
def trigger_send_kbs():
    # print("===> Task Triggered")
    # now = datetime.now()
    # yesterday = now - timedelta(days=20)
    # unprocessed_kbs = KnowledgeBase.objects.filter(Q(created_at__gte=yesterday) & Q(processed=False) & Q(import_batch_id__isnull=True))[:3]
    # print("ssssssssssssssssss", unprocessed_kbs)
    # for kb in unprocessed_kbs:
    #     # send_kb_to_ai.delay(kb.id)
    #     send_kb_to_ai.apply_async(args=[kb.id], queue='queue_one')

    print("===> Task trigger_send_kbs_is_triggered")
    unchecked_statuses = KnowledgeBaseProcessStatus.objects.filter(
        add_news_checking=False,
        add_news_check_failed=False,
        knowledge_base__import_batch_id__isnull=True,
        knowledge_base__processed=False,
        knowledge_base__is_news = True,

    ).select_related('knowledge_base', 'knowledge_base__source')[:4]
    for status in unchecked_statuses:
        status.add_news_checking = True
        status.save(update_fields=['add_news_checking'])
        send_kb_to_ai.apply_async(args=[status.knowledge_base.id], queue='queue_one')

@shared_task(bind=True, name='search.tasks.send_kb_to_ai')
def send_kb_to_ai(self, kb_id):
    try:
        with transaction.atomic():
            kb = KnowledgeBase.objects.select_for_update().get(id=kb_id)
            status = KnowledgeBaseProcessStatus.objects.select_for_update().get(knowledge_base=kb)

            truncated_body = kb.body[:3000]

            headers = {
                'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                'Content-Type': 'application/json',
            }

            payload = {
                'category': kb.category,
                'id': str(kb.id),
                'title': kb.title,
                'body': truncated_body,
            }
            json_data = {
                'source_uri': getattr(kb.source, 'source_uri', None) if kb.source else None,
                'relevance': getattr(kb, 'relevance', None),
                'Country': getattr(kb.source, 'country', None) if kb.source else None,
                'Affiliation': getattr(kb.source, 'affiliation', None) if kb.source else None,
                'PoliticalOrientation': getattr(kb.source, 'political_orientation', None) if kb.source else None,
                'Intensity': getattr(kb.source, 'intensity', None) if kb.source else None,
                'LinkedTo': getattr(kb.source.linked_to, 'name', None) if (kb.source and kb.source.linked_to) else None,
            }

            response = requests.post('http://89.42.199.251:5682/text/kb/add_news_auto_labeling',
                                        params=payload,
                                        json=json_data,
                                        headers=headers,
                                        timeout=(3, 60) # 3 ثانیه برای اتصال، 60 ثانیه برای خواندن
                                        )
            if  response.status_code != 200:
                    status.add_news_check_failed = True
                    status.add_news_checking = False
                    status.save(update_fields=['is_news_check_failed', 'is_news_checking'])
                    print(f"❌ Failed to translate title for kb {kb.id}")
                    return
            

            res = response.json()
            detected_cat = res.get("detected_cat")

            # map real/fake به label_id
            label_map = {
                "real": 1,
                "fake": 2
            }
            label_id = label_map.get(detected_cat.lower()) if detected_cat else None

            if not label_id:
                print(f"⚠️ No valid detected_cat for kb.id = {kb.id}")
            
            try:
                label = Label.objects.get(id=label_id)
            except Label.DoesNotExist:
                print(f"❌ Label with id={label_id} not found for kb.id = {kb.id}")
                return
            ai_client = get_ai_client()

            KnowledgeBaseLabelUser.objects.create(
                knowledge_base_id=kb.id,
                label_id=label_id,
                user_id=ai_client.id
            )
            kb.processed = True
            kb.default_label = label
            kb.save(update_fields=['processed', 'default_label'])
            # print("✅ API sent for kb.id =", kb.id)
            print(f"✅ Label {detected_cat} assigned to kb.id = {kb.id}")
            
    
    except KnowledgeBase.DoesNotExist:
        print(f"❌ KnowledgeBase with id={kb_id} not found.")
    except Exception as e:
        print(f"❌ Unexpected error for kb_id={kb_id}: {e}")
    
# @shared_task(bind=True, name='search.tasks.send_kb_to_ai')
# def send_kb_to_ai(self, kb_id):
#     try:
#         kb = KnowledgeBase.objects.select_for_update().get(id=kb_id)
#         status = KnowledgeBaseProcessStatus.objects.select_for_update().get(knowledge_base=kb)

#         truncated_body = kb.body[:3000]

#         headers = {
#             'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
#             'Content-Type': 'application/json',
#         }

#         payload = {
#             'category': kb.category,
#             'id': str(kb.id),
#             'body': truncated_body,
#         }
#         response = requests.post('http://89.42.199.251:5682/text/kb/add_news',
#                                     params=payload,
#                                     headers=headers,
#                                     timeout=(3, 60) # ← 3 ثانیه برای اتصال، 60 ثانیه برای خواندن
#                                     )
#         if response.status_code == 200:
#             kb.processed = True
#             kb.save()
#             print("✅ API sent for kb.id =", kb.id)
#         else:
#             # print(f"❌ Failed to send kb {kb.id}")
#             print(f"❌ Failed to send kb {kb.id}, Status: {response.status_code}, Response: {response.text}")
#             raise self.retry(exc=Exception(f"Status {response.status_code}"), countdown=30)
    
#     except Exception as exc:
#         raise self.retry(exc=exc,  countdown=30)
    

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
    process_news_batch.apply_async(args=[str(first_unprocessed)], queue='queue_three')


from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

@shared_task(name='search.tasks.process_news_batch')
def process_news_batch(batch_id):  
    print("===> Task Triggered")
    ai_client = get_ai_client()

    kb = KnowledgeBase.objects.filter(processed=False, import_batch_id=batch_id).first()
    if not kb:
        print("❌ kb failed")
        return
    # for kb in kb_list:
    ai_result = call_check_news_api(kb)
    if not ai_result:
        print("❌ ai_result failed")
        return
    
    search_item = save_search_item(ai_client, kb, batch_id)
    if not search_item:
        print("❌ search_item failed")
        return

    fact_data, chart_data = build_chart_data(ai_result)

    combined_result = {
        'id': str(search_item.id),
        'search_text': kb.body,
        'ai_result': ai_result,
        'fact_data': fact_data,
        'chart_data': chart_data
    }

    search_item.result = "real" if ai_result.get('result') == "real" else "fake"
    search_item.processed = True
    search_item.ai_answer = combined_result
    search_item.save()
    update_labels(kb, ai_client, ai_result)
        
        
# @shared_task(name='search.tasks.check_is_news_from_ai')
# def check_is_news_from_ai():
#     print("===> Task check_is_news_from_ai_is_triggered")
#     unchecked_news  = KnowledgeBase.objects.filter(
#         is_news__isnull=True, 
#         is_news_check_failed=False
#             )[:4]

#     print("unchecked_news", unchecked_news)
#     for kb in unchecked_news:
#         # process_unchecked_news.delay(kb.id)
#         process_unchecked_news.apply_async(args=[kb.id], queue='queue_two')


# @shared_task(bind=True, name='search.tasks.process_unchecked_news')
# def process_unchecked_news(self, kb_id):
#     try:
#         with transaction.atomic():
#             kb = KnowledgeBase.objects.get(id=kb_id)

#             def call_api(input_text):
#                 headers = {
#                     'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
#                     'Content-Type': 'application/json',
#                 }
#                 payload = {'input_news': input_text}
#                 try:
#                     response = requests.post(
#                         'http://89.42.199.251:5682/text/is_news',
#                         params=payload,
#                         headers=headers,
#                         timeout=(3, 45)
#                     )
#                     return response
#                 except requests.RequestException as e:
#                     print(f"❌ Exception while calling API: {e}")
#                     return None

#             # First request: with title
#             response_title = call_api(kb.title)
#             if response_title is None or response_title.status_code != 200:
#                 kb.is_news_check_failed = True
#                 kb.save()
#                 print(f"❌ Failed to translate title for kb {kb.id}, Status: {getattr(response_title, 'status_code', 'N/A')}")
#                 return

#             data = response_title.json()
#             kb.is_news = data.get("result")
#             kb.title = data.get("trans")

#             # Second request: with truncated body
#             truncated_body = kb.body[:3000]
#             response_body = call_api(truncated_body)
#             if response_body is None or response_body.status_code != 200:
#                 kb.is_news_check_failed = True
#                 kb.save()
#                 print(f"❌ Failed to translate body for kb {kb.id}, Status: {getattr(response_body, 'status_code', 'N/A')}")
#                 return

#             trans_body = response_body.json().get("trans")
#             kb.body = trans_body

#             kb.is_news_check_failed = False  # موفقیت‌آمیز
#             kb.save()
#             print("✅ is_news, title & body checked and saved for kb.id =", kb.id)

#     except KnowledgeBase.DoesNotExist:
#         print(f"❌ KnowledgeBase with id={kb_id} not found.")
#     except Exception as e:
#         print(f"❌ Unexpected error for kb_id={kb_id}: {e}")

@shared_task(name='search.tasks.check_is_news_from_ai') 
def check_is_news_from_ai():
    print("===> Task check_is_news_from_ai_is_triggered")

    # unchecked_statuses = KnowledgeBaseProcessStatus.objects.filter(
    #     is_news_checking=False,
    #     is_news_check_failed=False,
    #     knowledge_base__is_news__isnull=True
    # ).select_related('knowledge_base')[:4] 
    # 
    unchecked_statuses = KnowledgeBaseProcessStatus.objects.filter(
        is_news_checking=False,
        is_news_check_failed=False,
        knowledge_base__is_news__isnull=True,
        knowledge_base__lang='eng'
    ).select_related('knowledge_base')[:4]

    print("cccccccccccccccccccccccc", unchecked_statuses)
    for status in unchecked_statuses:
        status.is_news_checking = True
        status.save(update_fields=['is_news_checking'])
        process_unchecked_news.apply_async(args=[status.knowledge_base.id], queue='queue_two')


@shared_task(bind=True, name='search.tasks.process_unchecked_news')
def process_unchecked_news(self, kb_id):
    try:
        with transaction.atomic():
            kb = KnowledgeBase.objects.select_for_update().get(id=kb_id)
            status = KnowledgeBaseProcessStatus.objects.select_for_update().get(knowledge_base=kb)

            def call_api(input_text):
                headers = {
                    'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
                    'Content-Type': 'application/json',
                }
                payload = {'input_news': input_text}
                try:
                    response = requests.post(
                        'http://89.42.199.251:5682/text/is_news',
                        params=payload,
                        headers=headers,
                        timeout=(3, 60)
                    )
                    return response
                except requests.RequestException as e:
                    print(f"❌ Exception while calling API: {e}")
                    return None

            # First request: with title
            response_title = call_api(kb.title)
            if response_title is None or response_title.status_code != 200:
                status.is_news_check_failed = True
                status.is_news_checking = False
                status.save(update_fields=['is_news_check_failed', 'is_news_checking'])
                print(f"❌ Failed to translate title for kb {kb.id}")
                return

            data = response_title.json()
            kb.is_news = data.get("result")
            kb.title = data.get("trans")

            # Second request: with truncated body
            truncated_body = kb.body[:3000]
            response_body = call_api(truncated_body)
            if response_body is None or response_body.status_code != 200:
                status.is_news_check_failed = True
                status.is_news_checking = False
                status.save(update_fields=['is_news_check_failed', 'is_news_checking'])
                print(f"❌ Failed to translate body for kb {kb.id}")
                return

            trans_body = response_body.json().get("trans")
            kb.body = trans_body
            kb.save(update_fields=["is_news", "title", "body"])

            status.is_news_check_failed = False
            status.is_news_checking = False
            status.save(update_fields=['is_news_check_failed', 'is_news_checking'])
            print("✅ is_news, title & body checked and saved for kb.id =", kb.id)

    except KnowledgeBase.DoesNotExist:
        print(f"❌ KnowledgeBase with id={kb_id} not found.")
    except Exception as e:
        print(f"❌ Unexpected error for kb_id={kb_id}: {e}")


