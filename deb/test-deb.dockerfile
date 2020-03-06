FROM debian:stable

# get jre 8 installed - only 11 is available in default image
RUN apt-get update && apt-get upgrade -y && apt-get install -y wget gnupg software-properties-common
RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add
RUN add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
RUN apt-get update && apt-get install -y adoptopenjdk-8-hotspot

COPY . /data
VOLUME /data
WORKDIR /data

# still can't run systemd in docker image - no joy
