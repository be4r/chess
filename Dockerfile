FROM ubuntu:latest
RUN useradd user
WORKDIR /home/user
COPY ./ ./
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt update && apt install -y python3 python3-pip python3-tk
RUN pip3 install playsound Pillow
RUN apt install python-gi python3-gi pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev
ENTRYPOINT bash

