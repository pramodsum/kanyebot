FROM python:3.5.1-slim
ADD . /src
WORKDIR /src

RUN apt-get update
RUN apt-get install -y make
RUN apt-get install -y gcc
RUN apt-get install -y libxslt-dev libxml2-dev
RUN apt-get install -y wget git-core

RUN pip install -r requirements.txt
CMD python ./bot/app.py
