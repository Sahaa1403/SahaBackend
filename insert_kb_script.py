import requests
from datetime import datetime

# Replace with your actual base URL and authentication token if needed
BASE_URL = "{{base_url}}"
CREATE_SOURCE_URL = f"{BASE_URL}/api/v1/search/kb/sources"
CREATE_KB_URL = f"{BASE_URL}/api/v1/search/kb/knowledgebase"

# Optional headers, add authentication if needed
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_API_TOKEN"
}

data = {
    "data": [
        {
            "source": "BBC News",
            "body": "Saka scores 'magnificent' goal as Arsenal beat Real Madrid...",
            "publishedAt": "2025-04-16T21:00:51Z",
            "url": "https://www.bbc.com/sport/football/videos/cz95j3144eko"
        },
        {
            "source": "BBC News",
            "body": "PSG come from behind to claim impressive win over Villa...",
            "publishedAt": "2025-04-09T21:16:22Z",
            "url": "https://www.bbc.com/sport/football/videos/cwynn7zq94po"
        },
        {
            "source": "BBC News",
            "body": "'Aston Villa bucked the trend in January - and are reaping rewards'...",
            "publishedAt": "2025-04-02T23:34:51Z",
            "url": "https://www.bbc.com/sport/football/articles/cjr741wgyn9o"
        },
        {
            "source": "BBC News",
            "body": "De Bruyne to leave Manchester City at end of season...",
            "publishedAt": "2025-04-04T11:01:07Z",
            "url": "https://www.bbc.com/sport/football/articles/cj3x0jpmgv4o"
        },
        {
            "source": "By Bret Stephens",
            "body": "- هنگام ارائه از نوک شمشیر ، یک شاخه زیتون آسان تر است.",
            "publishedAt": "2025-04-15T20:14:29Z",
            "url": "https://www.nytimes.com/2025/04/15/opinion/iran-trump-nuclear-deal.html"
        }
    ]
}

# A simple cache to avoid recreating sources multiple times
source_id_cache = {}

for item in data["data"]:
    source_name = item["source"]

    # Check if source already created
    if source_name not in source_id_cache:
        source_payload = {
            "title": source_name
        }
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

    # Prepare knowledge_base payload
    kb_payload = {
        "title": item["body"],
        "source": source_id,
        "created_at": item["publishedAt"]
    }

    kb_response = requests.post(CREATE_KB_URL, json=kb_payload, headers=headers)
    if kb_response.status_code == 200:
        print(f"KnowledgeBase entry created for: {item['body'][:30]}...")
    else:
        print(f"Failed to create knowledge base for '{item['body'][:30]}...'. Response: {kb_response.text}")
