
pushd "%~dp0"
python manage.py migrate
python manage.py loaddata db.json
popd