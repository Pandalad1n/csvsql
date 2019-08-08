FROM python:3.6

RUN apt-get update \
 && apt-get install -y postgresql \
 && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
