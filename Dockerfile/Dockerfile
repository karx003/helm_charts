FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir Flask pymongo

EXPOSE 5000

CMD ["python", "app.py"]

