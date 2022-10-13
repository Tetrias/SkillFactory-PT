FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /project_django

COPY requirements.txt /project_django/

RUN pip install -r requirements.txt

ADD . /project_django/
