pip install virtualenv
python3 -m venv venv
. venv/bin/activate
pip install requirements.txt
export FLASK_ENV=development
python3 app.py
