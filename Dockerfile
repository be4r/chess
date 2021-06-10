FROM ubuntu:latest
RUN useradd user
WORKDIR /home/user
COPY ./ ./
ENV DEBIAN_FRONTEND="noninteractive"
RUN apt update && apt install -y python3 python3-pip python3-tk python3-babel python3-pil.imagetk
RUN pip3 install playsound Pillow
WORKDIR /home/user/chess 
ENTRYPOINT python3 main.py

