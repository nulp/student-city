::%~dp0python-3.7.3.exe
::start pip install -r requirements.txt
pushd "%~dp0"
::pip install django python-dateutil django-extensions whitenoise unidecode djangorestframework markdown django-filter
pip freeze > requirements.txt
::python manage.py runserver
popd
pause