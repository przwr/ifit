startdj:
    uwsgi uwsgi.ini --module ifitchallenge.wsgi -d log.txt
stopdj:
    uwsgi --stop uwsgi.pid
startdb:
    pg_ctl -D db -l dblog.txt start
stopdb:
    pg_ctl -D db