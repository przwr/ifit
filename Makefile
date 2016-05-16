start:
	uwsgi uwsgi.ini --module ifitchallenge.wsgi -d log.txt
stop:
	uwsgi --stop uwsgi.pid
startdb:
	pg_ctl -D db -l dblog.txt -o '-p 5333' start
stopdb:
	pg_ctl -D db stop
wait:
	sleep 2 
restart: stop wait start
