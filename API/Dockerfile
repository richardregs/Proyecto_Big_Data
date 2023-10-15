FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
ENV DEBUG True
RUN apt update
RUN ln -sf /usr/share/zoneinfo/America/Lima /etc/localtime

RUN mkdir /API
WORKDIR /API
COPY API ./API
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
WORKDIR /API