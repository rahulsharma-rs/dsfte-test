FROM alpine:latest
FROM python:3.10-slim-buster

WORKDIR /dsfet-test/app

COPY ./app /dsfet-test/app
RUN pip install -r /dsfet-test/app/requirements.txt

RUN pip install gunicorn

ENV FLASK_APP=/dsfet-test/app/app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
