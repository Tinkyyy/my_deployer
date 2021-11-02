FROM ubuntu:18.04

COPY . /app
WORKDIR /app

RUN apt update && apt install -y \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD python3 app.py
