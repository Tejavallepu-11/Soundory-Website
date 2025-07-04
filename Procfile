web: gunicorn Soundory.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn Soundory.wsgi