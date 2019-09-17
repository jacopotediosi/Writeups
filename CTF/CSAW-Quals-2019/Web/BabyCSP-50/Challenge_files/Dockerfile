FROM ubuntu:18.04
MAINTAINER tnek
RUN apt-get update
RUN apt-get install -y firefox python python-pip
COPY geckodriver /usr/local/bin
COPY requirements.txt .

RUN chmod 777 /usr/local/bin/geckodriver && pip install -r requirements.txt && pip install gunicorn

COPY /chal /chal
WORKDIR /chal

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]