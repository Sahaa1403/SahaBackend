from mongoengine import connect
import os
from django.http import HttpResponse


MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = "lhotse.liara.cloud"
MONGO_PORT = 30800


def check_mongodb_connection(request):
    try:
        connect(
            db=MONGO_DB,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            host=f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
        )
        return HttpResponse("MongoDB connection successful")
    except Exception as e:
        return HttpResponse(f"MongoDB connection failed: {e}")