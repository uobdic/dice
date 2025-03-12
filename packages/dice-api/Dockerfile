FROM python:3.11.6-slim

RUN apt update && apt install -y git wget
RUN wget https://apt.puppet.com/puppet-release-jammy.deb \
 &&  dpkg -i puppet-release-jammy.deb \
 && apt update && apt install -y puppet-agent
# Path: /app
WORKDIR /app

ADD ./ /app/.

# TODO: this will change to install from pypi
RUN pip install --no-cache-dir .

ENV PATH="/opt/puppetlabs/bin:${PATH}"
CMD ["dice-api"]
