FROM python:3.8

WORKDIR /Norwood

COPY . /Norwood

RUN pip install -r requirements.txt

