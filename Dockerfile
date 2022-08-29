FROM python:3.10-slim

WORKDIR /wildfires_project

RUN apt-get update
RUN python -m pip install --upgrade pip
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /.kaggle  /root/.kaggle

COPY . .

RUN kaggle datasets download -d rtatman/188-million-us-wildfires

RUN apt-get install -y unzip && \
    unzip 188-million-us-wildfires.zip

