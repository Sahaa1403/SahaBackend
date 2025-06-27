from django.apps import AppConfig
from mongoengine import connect
import os



class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'

    def ready(self):
        MONGO_DB = os.getenv("MONGO_DB")
        MONGO_USER = os.getenv("MONGO_USER")
        MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
        MONGO_HOST = "lhotse.liara.cloud"
        MONGO_PORT = 30800
        import search.signals  # این خط سیگنال رو فعال می‌کنه

        connect(
            db=MONGO_DB,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            host=f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
        )