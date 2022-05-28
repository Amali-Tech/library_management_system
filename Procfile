web : gunicorn library.wsgi
config: set DEBUG_COLLECTSTATIC=1
release: python3 manage.py makemigrations --noinput
release: python3 manage.py collectstatic --noinput
release: python3 manage.py migrate --noinput