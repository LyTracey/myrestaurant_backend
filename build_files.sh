# Install dependencies
pwd
ls

pip install --upgrade pip
apt-get --version
apt-get install pkg-config
pip install -r requirements.txt

# Make migrations
python3.9 manage.py makemigrations
python3.9 manage.py migrate

# Collect static files 
python3.9 manage.py collectstatic