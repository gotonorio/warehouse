# warehouse用Dockerfile by N.Goto
# 使用するベースイメージ。
FROM python:3.13-slim
# stdoutへの出力をバッファリングさせない。(errorやlogを直ちに出力して欲しいから)
ENV PYTHONUNBUFFERED=1
# /code/ディレクトリを作業用ディレクトリにする。
WORKDIR /code
# requirements.txtファイルを/code/ディレクトリにコピーする。
COPY requirements.txt /code/
# weasyprintのためのlibraliesをインストールする
RUN apt-get -y update \
    && apt-get install -y \
    python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 \
    fonts-noto-cjk \
    && apt-get -y clean
# pipでpythonパッケージをインストールする。
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --requirement requirements.txt
# ホスト上のdjangoアプリ、データベースファイルなどを/code/ディレクトリにコピーする。
# しかしCOPYコマンドでは、親ディテクトリはコピーできないので、docker-composeでmountする。
# または、Dockerfileを親ディレクトリと同じ階層に配置して、djangoソースをコンテナ内にコピーする。
# COPY . /code/
