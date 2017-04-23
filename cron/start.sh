#!/bin/sh

rsyslogd && crond
tail -F /var/log/cron.log
