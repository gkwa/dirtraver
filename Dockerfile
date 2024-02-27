FROM python:latest

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_lg
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en

RUN mkdir -p /tmp/src
COPY main.py /tmp/src

