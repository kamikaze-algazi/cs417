# Hello World
## Alyx & Sunny CS417 Databases Project

### Setup
1. Ensure you have python 2 installed, and that a 'python2' syslink exists in the path.
2. Create a PSQL user with any name and password. Create a file in the ~/.secrets/ directory called 'psqlauth.py'. Inside this file, copy paste the following:
```
user='PsqlUname'
pw='PsqlPword'
db='PsqlDbase'
```
    replacing the quoted text items with the correct values.

3. Using the command pip2 install PACKNAME, install the following packages
    * jinja2
    * passlib
    * web.py
4. Change the second line of the 'run' script to reflect your postgres password.
5. Move the directory to ~/public_html/wsgi
6. In the wsgi directory, type './run'
