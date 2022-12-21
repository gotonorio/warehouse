# 使用するベースイメージ。
FROM python:3-alpine
# stdoutへの出力をバッファリングさせない。(errorやlogを直ちに出力して欲しいから)
ENV PYTHONUNBUFFERED 1
# コンテナ環境にディレクトリを作成しておく。
RUN mkdir /code
# /code/ディレクトリを作業用ディレクトリにする。
WORKDIR /code
# requirements.txtファイルを/code/ディレクトリにコピーする。
COPY requirements.txt /code/
# コンパイル環境をインストールする。
RUN apk add --update --no-cache g++ gcc \
            libc-dev \
            libstdc++ \
            make \
            openblas-dev \
            jpeg-dev \
            zlib-dev
# alpineでTimeZoneをJSTにするための追加処理。
# https://qiita.com/dtan4/items/8359e389b95cbc60952d#タイムゾーンの設定
RUN apk --update add tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    echo "Asia/Tokyo" > /etc/timezone
# pipコマンドを実行してrequirements.txtに記載してあるライブラリをインストールする。
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# ホスト上のdjangoアプリ、データベースファイルなどを/code/ディレクトリにコピーする。
# https://docs.docker.com/compose/django/#define-the-project-components
COPY . /code/
