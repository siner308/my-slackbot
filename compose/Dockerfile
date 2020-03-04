FROM python:3.5

ENV TZ="Asia/Seoul"

RUN apt-get update && apt-get autoremove && apt-get autoclean \
    && apt-get install -y \
      tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./app /app
COPY ./compose/start /start

RUN chmod +x /start
 
WORKDIR /app

ENTRYPOINT /start
