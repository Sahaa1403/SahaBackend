from search.models import KnowledgeBaseLabelUser, KnowledgeBaseProcessStatus, Label
from search.models import KnowledgeBase
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from accounts.models import User
import requests
from search.serializers import KnowledgeBaseSerializer, SearchSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction


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

def get_ai_client():
    return User.objects.get_or_create(
        email="ai_client@yourapp.com",
        defaults={
            "username": "ai_client",
            "name": "ai client",
            "is_active": False,
            "password": make_password(get_random_string(12)),
        }
    )[0]

def call_check_news_api(kb):
    headers = {
        'sahaa-ai-api': 'WGhgR5dOAEc34MI0Zpi5C2Y3LyjwT9Ex',
        'Content-Type': 'application/json',
    }
    payload = {'input_news': kb.body}

    try:
        # response = requests.post(
        #     "http://62.60.198.225:5682/text/check_news",
        #     params=payload,
        #     headers=headers,
        #     timeout=60
        # )
        response = requests.post(
            "http://89.42.199.251:5682/text/check_news",
            params=payload,
            headers=headers,
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        print(f"❌ Failed API call for kb.id={kb.id} - status={response.status_code}")
    except Exception as e:
        print(f"❌ Exception calling API for kb.id={kb.id} - {e}")
    return None


def save_search_item(ai_client, kb, batch_id):

    search_data = {'user': ai_client.id, 'text': kb.body, 'import_batch_id': batch_id}
    serializer = SearchSerializer(data=search_data)

    if serializer.is_valid():
        search_item = serializer.save()
        print(f"[SEARCH] Search item saved with id={search_item.id}")
        return search_item
    print("❌[SEARCH] Failed to save search item", serializer.errors)
    return None


def build_chart_data(ai_result):
    try:
        fact_id = ai_result.get("fact_id")
        fact = KnowledgeBase.objects.filter(id=fact_id).first()
        if not fact:
            print("❌ fact_data not found")
            return None, {"pie_chart": None, "radar_chart": None}
        fact_data = KnowledgeBaseSerializer(fact).data

        similar_kbs = KnowledgeBase.objects.filter(
            id__in=ai_result.get('simmilar_news', [])
        ).select_related('source', 'social_media')

        counts = {"foreign_social": 0, "foreign_sites": 0, "internal_social": 0, "internal_sites": 0}
        for kb in similar_kbs:
            if kb.social_media:
                if kb.social_media.origin_type == "foreign":
                    counts["foreign_social"] += 1
                elif kb.social_media.origin_type == "domestic":
                    counts["internal_social"] += 1

            if kb.source:
                if kb.source.origin_type == "foreign":
                    counts["foreign_sites"] += 1
                elif kb.source.origin_type == "domestic":
                    counts["internal_sites"] += 1

        total = len(similar_kbs) or 1
        radar_chart = {k: round(v / total * 100, 2) for k, v in counts.items()}

        lbls = [
            {
                "name": lbl["label_name"],
                "count": lbl["count"],
                "percentage": round((lbl["count"] / len(fact_data["labels"])) * 100, 2)
            }
            # for lbl in fact_data["labels"]
            for lbl in fact_data.get("labels", [])
        ]

        return fact_data, {"pie_chart": lbls, "radar_chart": radar_chart}
    except Exception as e:
        print("⚠️ build_chart_data failed:", e)
        return None, {"pie_chart": None, "radar_chart": None}


LABEL_MAPPING = {
    "real": "حقیقت",
    "mis": "نادرست",
    "dis": "فریب‌دهی",
    "mal": "مخرب",
}
def update_labels(kb, ai_client, ai_result):
    percentages = ai_result.get("percentages", {})
    if not percentages:
        print("❌ percentages failed")
        return

    max_label = max(percentages, key=percentages.get)
    label_title = LABEL_MAPPING.get(max_label)
    if not label_title:
        return

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