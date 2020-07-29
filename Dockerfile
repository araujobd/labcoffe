FROM python:3.8-alpine

LABEL maintainer="bdantas47@hotmail.com"

# copia o arquivo para dentro do container
COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY app /app

WORKDIR /app

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "--access-logfile", "-", "app:app"]