FROM python:bookworm

RUN mkdir -p /tmp/src
WORKDIR /tmp/src
COPY requirements.txt /tmp/src

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_lg
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en

COPY . /tmp/src
