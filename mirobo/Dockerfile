FROM python:3.7-alpine
RUN apk add --no-cache libffi-dev openssl-dev gcc musl-dev linux-headers
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "./robo.py" ]