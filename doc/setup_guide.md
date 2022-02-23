# Setup Guide

## Step 1: Install mysql
Run `sudo apt-get install mysql-server`


## Step 2: Create database

Run `sudo mysql -u root -p` and then enter the following commands:
```
mysql>  CREATE DATABASE tolls_app_database;
mysql>  CREATE USER 'tolls_root'@'localhost' IDENTIFIED BY 'tolls1234';
mysql>  GRANT ALL PRIVILEGES ON tolls_app_database.* TO 'tolls_root'@'localhost';
mysql>  FLUSH PRIVILEGES;
mysql>  SET innodb_lock_wait_timeout=120;
mysql>  quit;
```


## Step 3: Setup venv and install required packages
Create a virtual enviroment and clone the project's code. Just replace /your/path/to/cli/parser.py with the absolute path that leads to the cli/parser.py in your computer and save the changes.
```
python -m venv env
source env/bin/activate
git clone  https://github.com/ntua/TL21-55/
```
Enter your github credentials and then navigate to the newly created folder with `cd TL21-55` and then run: download the project's dependencies with:
```
pip install -r requirements.txt
```

If you face problems with the installation of `mysqlclient`, run:

```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

## Step 4: Enable server to run over HTTPs
Run the following commands:
```
sudo apt-get install wget libnss3-tools
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64
sudo mv mkcert-v1.4.3-linux-amd64 /usr/bin/mkcert
chmod +x /usr/bin/mkcert
```
With `mkcert --version` ensure that the mkcert version is 1.4.3.
While in the TL21-55 folder run
```
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
```

## Step 5: Initialize database
Run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser (enter whatever username/password you like)
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
```


## Step 6: Setup CLI alias
If you want to use the CLI by writing `se2155 healtcheck` instead of `python cli/parser.py healthcheck`, add the following lines to the end of `~/.bashrc`:
```
SOFTENG_PROJECT_CLI_PATH=/your/path/to/cli/parser.py
alias se2155="python $SOFTENG_PROJECT_CLI_PATH"
```
Just replace `/your/path/to/cli/parser.py` with the absolute path that leads to the `cli/parser.py` in your computer and save the changes.

---
### Warning
If you want to deploy this app, use a different mysql username than 'tolls_root' and choose a strong password for your mysql user.
These credentials should be passes to `/tolls/setting.py`. Just search for `DATABASE` and replace the appropriate fields.
