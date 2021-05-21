# Ubuntu
Just run:
```
sudo apt install mysql-server
```


create user:
```
sudo mysql -u root

CREATE USER 'sad'@'localhost' IDENTIFIED BY 'sad_pass';
CREATE DATABASE SADProject DEFAULT CHARACTER SET 'utf8';
GRANT ALL PRIVILEGES ON SADProject . * TO 'sad'@'localhost';
```


to install mysql.connector on python:
```
python3 -m pip install mysql-connector-python
```
