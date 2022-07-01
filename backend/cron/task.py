# encoding: utf-8
from crontab import CronTab
cron = CronTab(user='root')
job = cron.new(command='python /home/app/backend/cron/updateBenchmark.py')
job.setall('0 10 * * *')

cron.write()