# !/bin/bash
export FLASK_APP=app
flask db migrate -m "Ajout de la table Celebrity"
echo "------attente--------"
flask db upgrade
echo "Database migration complete."