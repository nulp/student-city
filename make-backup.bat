
pushd "%~dp0"
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
popd