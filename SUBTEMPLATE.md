# Targets

# in "created cont."
apt update
apt upgrade
apt install nginx-light
apt install php-fpm php-cli php-mysql

# setup logs
apt install rsyslog rsyslog-gnutls logrotate

# ==========

apt install mariadb-server
mysql_secure_installation


# apt-get install apache2-utils
# htpasswd -c /etc/nginx/.htpasswd username

# curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar


# In "webproxy"


10.3.70.43