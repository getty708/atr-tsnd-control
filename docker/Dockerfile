# == Stage.1: Make requirements.txt by poetry ==
FROM python:3.8-slim as builder
WORKDIR /root/src/
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt > requirements.txt

# == Stage.2: Build Maim Images ==
FROM tensorflow/tensorflow:2.6.0-jupyter
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y \
    git \
    emacs \
    tmux \
    nfs-common \
    cifs-utils \
    wget \
    curl \
    build-essential \
    iputils-ping \
    net-tools \
    sudo
RUN apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV TZ Asia/Tokyo
RUN pip install --upgrade pip

# Make working directory
RUN mkdir /root/atr-tk/

# Install Python Packages
COPY --from=builder /root/src/requirements.txt .
RUN echo 'alias python=python3' >> ~/.bashrc
RUN pip install -r /home/bob/requirements.txt

# Change working directory
WORKDIR /root/atr-tk/
