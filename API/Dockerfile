FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
ENV DEBUG True
RUN apt-get update && apt-get install -y \
    libdbus-1-dev \
    pkg-config
RUN ln -sf /usr/share/zoneinfo/America/Lima /etc/localtime

RUN mkdir /API
WORKDIR /API
COPY src ./src
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /API/src