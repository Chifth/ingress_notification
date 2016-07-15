FROM ubuntu:14.04

RUN apt-get update \
    && apt-get install -y \
        git \
        python \
        python-pip \
        python3-pip

# Install supervisor & virtualenv
RUN pip install supervisor && pip3 install virtualenv

# Get source
RUN git clone https://github.com/hsiuhsiu/ingress_notification.git /root/ingress \
    && cd /root/ingress \
    && virtualenv env
    && env/bin/pip install -r requirements.txt

WORKDIR /root/ingress
CMD ["env/bin/python", "main.py"]
