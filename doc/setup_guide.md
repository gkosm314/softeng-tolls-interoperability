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
mysql>  SER innodb_lock_wait_timeout=120;
mysql>  quit;
```


## Step 3: Create a new folder and navigate to it. Then run:
Create a virtual ust replace /your/path/to/cli/parser.py with the absolute path that leads to the cli/parser.py in your computer and save the changes.enviroment and clone the project's code.
```
python -m venv env
source env/bin/activate
git clone  https://github.com/ntua/TL21-55/
```
Enter your github credentials and then download the project's dependencies with:
```
pip install -r requirements.txt
```

If you face problems with the installation of `mysqlclient`, run:
`sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`


## Step 4: Initialize database
Go to the newly created folder with `cd TL21-55` and then run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser (enter whatever username/password you like)
python manage.py runserver
```


## Step 5: Setup CLI alias
If you want to use the CLI by writing se2155 healtcheck instead of python parser.py healthcheck, add the following lines to the end of `~/.bashrc`:
```
SOFTENG_PROJECT_CLI_PATH=/your/path/to/cli/parser.py
alias se2155="python $SOFTENG_PROJECT_CLI_PATH
```
Just replace `/your/path/to/cli/parser.py` with the absolute path that leads to the `cli/parser.py` in your computer and save the changes.

---
### Warning
If you want to deploy this app, use a different mysql username than 'tolls_root' and choose a strong password for your mysql user.
These credentials should be passes to `/tolls/setting.py`. Just search for `DATABASE` and replace the appropriate fields.
