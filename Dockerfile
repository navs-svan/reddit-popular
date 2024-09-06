FROM python:3.11.2

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app/

WORKDIR /app/reddit_ph/reddit_ph

CMD ["scrapy", ]
