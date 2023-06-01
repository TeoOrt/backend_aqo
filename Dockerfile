FROM python:3.10.6


RUN apt-get update && \
    apt-get install -y awscli

WORKDIR /app

COPY requirements.txt . 

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . .



EXPOSE 5000


CMD ["python", "app.py"]

