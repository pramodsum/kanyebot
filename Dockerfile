FROM python:2.7.11
ADD . /src
WORKDIR /src
RUN apt-get install python2.7-dev
RUN pip install -r requirements.txt
CMD python ./bot/app.py
