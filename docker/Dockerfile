FROM tensorflow/tensorflow:1.4.0-py3
MAINTAINER Yoshimura Naoya <yoshimura.napya@outlook.com>

# Emacsのインストール
RUN apt-get update
RUN apt-get install emacs24-nox -y

# git
RUN apt install git -y \
    && git config --global user.email "yoshimura.naoya@ist.osaka-u.ac.jp" \
    && git config --global user.name "Yoshimura Naoya" \
    && git config --global core.editor 'emacs -nw'


# 作業ディレクトリ
RUN mkdir /root/work/
WORKDIR /root/work/

# 追加python モジュール
COPY requirements.txt /root
RUN pip install --upgrade pip
RUN pip install -r /root/requirements.txt


