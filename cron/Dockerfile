FROM python:3.5-alpine

USER root

RUN apk update && \
    apk add --no-cache --update \
        openssh-client \
        alpine-sdk \
        rsyslog \
        build-base

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

COPY requirements /tmp/requirements
RUN pip install -r /tmp/requirements/pip.txt

COPY . /cron
WORKDIR /cron

RUN crontab crontab
RUN touch /var/log/cron.log

RUN chmod +x /cron/start.sh

CMD ["/cron/start.sh"]
