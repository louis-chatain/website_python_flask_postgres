export FLASK_APP=app
echo "------going to migrate--------"
flask db migrate -m "modiciation of the Celebrity Class"
echo "------going to upgrade--------"
flask db upgrade
echo "Database migration complete."