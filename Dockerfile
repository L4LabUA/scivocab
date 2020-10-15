FROM ubuntu:20.04

run apt-get update
run apt-get -y install python3-pip
EXPOSE 5001

COPY . /scivocab
WORKDIR /scivocab
RUN pip3 install -r requirements.txt
ENV FLASK_APP=run.py
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5001"]
