FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]