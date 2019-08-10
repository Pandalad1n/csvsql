FROM python:3.6

RUN apt-get update \
 && apt-get install -y postgresql \
 && apt-get clean

WORKDIR /app

ENV PYTHONPATH /app/app
ENV FLASK_APP /app/app/server.py

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0 --port 80
EXPOSE 80