FROM python:2.7-slim
ADD . /src
WORKDIR /src
RUN apt-get install python-dev
RUN pip install -r requirements.txt
CMD python ./bot/app.py
