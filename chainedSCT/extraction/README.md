## Python & PostgreSQL

Please consider this important note that you should be able to connect to your postgresql. Use this guidance to do so.
### installation and configuration 

https://help.ubuntu.com/community/PostgreSQL

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04
- Resources: https://gist.github.com/ddbs/d3c1f76f9963e79fff19
            https://linuxhint.com/postgresql_python/
 

install

		sudo apt-get update
		sudo apt-get install postgresql postgresql-contrib

open server

		sudo -u postgres psql postgres


set new password for the postgres user:

		\password postgres


quit postgres:

		\q


create new user 

		$ sudo sudo -u postgres createuser dario --interactive
		Shall the new role be a superuser? (y/n) n
		Shall the new role be allowed to create databases? (y/n) y
		Shall the new role be allowed to create more new roles? (y/n) n


create new database

		$ createdb dario

get into postgres command prompt

		psql

set new password

		\password



## resources

Postgres differentiates between single and double quotes, so it is best to stick to single quoting strings.

http://www.postgresql.org/docs/9.2/static/datatype.html#DATATYPE-TABLE


run sql code from file

		psql -d snippets < schema.sql
	
list databases

		\l

enter into specific database

		psql -d snippets

get information about a specific table

		\d+ table_name



## to access postgresql from python

		sudo apt-get install libpq-dev python3-dev

		sudo pip3 install virtualenv

		sudo python3 -m pip install psycopg2
		
		

- Now let’s see whether we can login to our newly created database pyapp using our login username with the following command:
```bash
$ psql --dbname=pyapp --password
```
Now type in the password that you set earlier for your PostgreSQL user and press <Enter>.
You should be logged in.

#### Installing psycopg2 with PIP and PIP3:
- Now it’s time to install psycopg2 Python module.

If you’re using Python 3, then run the following command to install psycopg2:
```bash
$ pip3 install psycopg2-binary
```
If you’re using Python 2, then run the following command to install psycopg2:
```bash
$ pip install psycopg2-binary
```
psycopg2-binary PIP module should be installed.

- Creating the Project Directory:
Now create a project directory, pyapp with the following command:
```bash
$ mkdir pyapp
```
And navigate to the directory with the following command:
```bash
$ cd pyapp
```
This is where I will create all the Python script to access PostgreSQL database.

- Connecting to the PostgreSQL Database:
First, create a python program connect.py in your project directory. You can see the connect.py, create_table.py, insert_date.py and print_data.py as reference to start your code.

while you are connected to the database you are good to go for the several tests.