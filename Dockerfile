FROM python:3.10

LABEL maintainer="Nikita Orlov <orlov.nickita@gmail.com>"

RUN apt-get update -y
RUN apt-get upgrade -y

RUN mkdir ./app

COPY . /app

WORKDIR ./app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python3", "main.py"]