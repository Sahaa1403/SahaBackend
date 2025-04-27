import requests
from datetime import datetime
import json
import time

BASE_URL = "https://sahabackend.liara.run"
CREATE_SOURCE_URL = f"{BASE_URL}/api/v1/search/kb/sources"
CREATE_KB_URL = f"{BASE_URL}/api/v1/search/kb/knowledgebase"
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_API_TOKEN"
}

with open('KB-init.json', 'r') as file:
    data = json.load(file)


# A simple cache to avoid recreating sources multiple times
source_id_cache = {}

for item in data["data"]:
    print("=====================================")
    source_name = item["source"]

    # Check if source already created
    if source_name not in source_id_cache:
        source_payload = {
            "title": source_name
        }
        time.sleep(2)
        source_response = requests.post(CREATE_SOURCE_URL, json=source_payload, headers=headers)
        if source_response.status_code == 200:
            source_id = source_response.json()["id"]
            source_id_cache[source_name] = source_id
            print(f"Source '{source_name}' created with ID: {source_id}")
        else:
            print(f"Failed to create source '{source_name}'. Response: {source_response.text}")
            continue  # Skip to next item if source creation fails
    else:
        source_id = source_id_cache[source_name]


    dt = datetime.fromisoformat(item["publishedAt"].replace('Z', '+00:00'))
    kb_payload = {
        "title": f"{item['body'][:25]}...",
        "body": item["body"],
        "category": "real",
        "url": item["url"],
        "source": source_id,
        "created_at": dt.isoformat()
    }
    time.sleep(1)
    kb_response = requests.post(CREATE_KB_URL, json=kb_payload, headers=headers)
    if kb_response.status_code == 201:
        print(f"KnowledgeBase entry created for: {item['body'][:30]}...")
    else:
        print(f"Failed to create knowledge base for '{item['body'][:10]}...'. Response: {kb_response.text}")