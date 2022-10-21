sudo systemctl start nginx
sudo systemctl start postgresql
gunicorn -b 127.0.0.1:8000 --workers=4 web.wsgi
