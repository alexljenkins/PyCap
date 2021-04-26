FROM python:3.8.9-slim
RUN apt-get -y update
ADD requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /opt/working