FROM python:3.11.5

# تنظیمات اولیه
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# دایرکتوری اپ
ENV APP_HOME=/app
WORKDIR $APP_HOME
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    tk-dev \
    tcl-dev \
    libxslt1-dev \
 && rm -rf /var/lib/apt/lists/*

# نصب pip و پکیج‌ها
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# کپی سورس کد
COPY . $APP_HOME


# پورت
EXPOSE 8000

# اجرای جنگو
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
