#!/bin/bash
echo "$(date): " >> /var/log/cron.log 2>&1
/usr/local/bin/python /usr/src/app/main.py >> /var/log/cron.log 2>&1