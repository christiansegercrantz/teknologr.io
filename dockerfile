# FROM python:3.10.12-ubuntu22.04.3
FROM ubuntu:22.04
USER root

#Required for older version of docker. Try removing first and if it works don't worry.
RUN sed -i -e 's/^APT/# APT/' -e 's/^DPkg/# DPkg/' \
    /etc/apt/apt.conf.d/docker-clean

RUN apt update
RUN apt install -y python3.10
RUN apt install -y python3-pip 
# RUN pip install --upgrade pip

RUN apt install -y  \
    libsasl2-dev  \
    python3-dev \
    libldap2-dev \
    libssl-dev \
    libpq-dev

RUN apt install -y git

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN ["python", "manage.py", "migrate"]

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "8888" ]