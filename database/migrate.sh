export FLASK_APP=app
echo "------going to migrate--------"
flask db migrate -m "Adding the Table User"
echo "------going to upgrade--------"
flask db upgrade
echo "Database migration complete."