FROM python:3.7-alpine

RUN apk add --no-cache bluez bluez-deprecated

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./miflora-mqtt-daemon.py" ]
