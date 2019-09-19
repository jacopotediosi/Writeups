FROM ubuntu:18.04

RUN apt update && apt install -y curl chromium-browser=76.* python python-pip

COPY requirements.txt .
COPY chromedriver /usr/local/bin

RUN chmod 777 /usr/local/bin/chromedriver && pip install -r requirements.txt

COPY /chal /chal
WORKDIR /chal

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

# Configure a healthcheck to verify that everything is up&running
HEALTHCHECK --interval=1m30s --timeout=10s --retries=2 CMD curl --silent --fail http://127.0.0.1:5000/ || exit 1
