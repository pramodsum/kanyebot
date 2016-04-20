FROM python:2.7.11
ADD . /src
WORKDIR /src
RUN apt-get install qt5-default libqt5webkit5-dev gstreamer1.0-plugins-base gstreamer1.0-tools gstreamer1.0-x
RUN pip install -r requirements.txt
CMD python ./bot/app.py
