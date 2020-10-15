FROM ubuntu:20.04

run apt-get update && apt-get -y install python3
EXPOSE 5000

COPY . /scivocab
WORKDIR scivocab
RUN ./tools/install
ENTRYPOINT ./tools/run_webapp_debug
