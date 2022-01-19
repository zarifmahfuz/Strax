FROM python:3.8-alpine

ARG PORT=4200
ENV PORT=$PORT

RUN mkdir /backend
COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENV=development