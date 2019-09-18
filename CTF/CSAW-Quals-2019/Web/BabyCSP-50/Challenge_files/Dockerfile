FROM ubuntu:18.04

RUN apt update && apt install -y curl firefox python python-pip

COPY requirements.txt .
COPY geckodriver /usr/local/bin

RUN chmod 777 /usr/local/bin/geckodriver && pip install -r requirements.txt && pip install gunicorn

COPY /chal /chal
WORKDIR /chal

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]

HEALTHCHECK --interval=1m30s --timeout=10s --retries=2 CMD curl --silent --fail http://127.0.0.1:5000/ || exit 1
