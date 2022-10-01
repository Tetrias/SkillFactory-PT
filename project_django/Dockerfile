FROM python:3.10

RUN pip install --upgrade pip

RUN mkdir /project_django

WORKDIR /project_django

COPY requirements.txt /project_django/

RUN pip install -r requirements.txt

ADD . /project_django/
