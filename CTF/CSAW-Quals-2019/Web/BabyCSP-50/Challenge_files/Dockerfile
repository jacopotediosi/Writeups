FROM alpine:latest

COPY requirements.txt .

RUN apk update && apk upgrade && apk add --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community curl chromium chromium-chromedriver python py-pip && pip install -r requirements.txt

COPY /chal /chal
WORKDIR /chal

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

# Configure an healthcheck to verify that everything is up&running
HEALTHCHECK --interval=1m30s --timeout=10s --retries=2 CMD curl --silent --fail http://127.0.0.1:5000/ || exit 1
