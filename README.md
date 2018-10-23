wp-setup
=====

## Description
WordPress is downloaded and it's arranged in a specific directory.  
Setting of DB and a presence of BASIC authentication can be established in config.ini.

## Usage

Edit config.ini
```
vi wp-setup/config.ini
---------------------------
# wp-setup config
[init]
# Wordpress setup directory.
path=/var/www/vhosts/test.com/public_html

# wordpress version
# version = latest => download wordpress latest version
# or version number
# version list => https://ja.wordpress.org/download/releases/
# default : latest
# ex) setup worespress for version 4.9.7
# version = 4.9.7
version = latest

# set owner and group for wordpress files and directories.
# unix user and unix group.
user = username
group = groupname

# Set Basic Auth
# true or false
# .htpasswd file is generated into an installation pass automatically.
basic_auth = false

[mysql]
dbname = database_name
user = user_name
password = user_password
---------------------------
```

exec
```
./wp-setup/wp-setup.py
```


## Install
```
wget https://gitlab01.z-hosts.com/nakano/wp-setup/repository/archive.zip -O wp-setup.zip && unzip wp-setup.zip -d wp-setup

```
