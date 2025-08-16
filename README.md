# Saha-Backend

### Saha API Services


[![](https://img.shields.io/badge/python-3.10-orange)](https://www.python.org/)
[![](https://img.shields.io/badge/Django-4.1-green)](https://www.djangoproject.com/)


## How to run

1. Clone this repository

```bash
git clone https://github.com/Sahaa1403/SahaBackend.git
```

2. Install dependencies

```bash
pip install -r requirements.txt 
```

3. Make .env file (use either prod.env.template or dev.env.template to create .env file)

4. Run the following commands to get started (Development)

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

5. Make sure you have Postgredb running (Production)

6. you can run them manually, after the containers spin up, like so:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate   
docker exec -it container_id python manage.py createsuperuser

```


7. Build the image and spin up the two containers

```bash
docker-compose up -d --build
```

everytime we want to get news from newsApi we call https://sahabackend.liara.run/api/v1/search/news/everything endpoint
and execute celery Beat with this command >> celery -A config beat --loglevel=info
and execute worker of celery with this command >> celery -A config worker --loglevel=info --queues=queue_one --pool=solo
and for specify the article type and translate articles run another worker with in a new queue with this command >> 
celery -A config worker --loglevel=info --queues=queue_two --pool=solo

