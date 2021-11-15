python manage.py makemigrations
if python manage.py showmigrations -p | grep -q "\[ \]"; then python manage.py migrate; fi
python manage.py runserver 0.0.0.0:8000
