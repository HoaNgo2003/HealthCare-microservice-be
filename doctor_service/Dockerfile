# Dockerfile
FROM python

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8006"]
