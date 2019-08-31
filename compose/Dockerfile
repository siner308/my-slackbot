FROM python:3.5

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./app /app
COPY ./compose/start /start

RUN chmod +x /start
 
WORKDIR /app

ENTRYPOINT /start
