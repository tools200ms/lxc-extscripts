#!/bin/bash

CONTAINER_NAME="srv.web.site-datm"

FSSIZE=2G

DIST="devuan"
RELEASE="daedalus"
ARCH="amd64"


function cra_print_help() {
  cat << EOF
$BASE_SCRIPT create <lxc cont. name> <ip addr> <gateway>
        create  - create new container
EOF
}

function op_create() {
  cname=$1
  ip_addr=$2
  gateway=$3

  $RUN lxc-create -n $cname \
        -B lvm --lvname $cname --vgname=$VGNAME --fssize=$FSSIZE\
        -f /etc/lxc/server.conf \
        -t download -- -d $DIST -r $RELEASE -a $ARCH


  if [ -z $RUN ]; then
    cat <<EOF >> /var/lib/lxc/$cname/config

# Container specific network configuration:
lxc.net.0.ipv4.address = $IP_ADDRESS
lxc.net.0.ipv4.gateway = $GATEWAY
EOF
  fi

  # mount
  MOUNT_DIR=/mnt/lxc/$CONTAINER_NAME
  $RUN mkdir -p $MOUNT_DIR
  $RUN mount /dev/mapper/$VGNAME-$cname $MOUNT_DIR

  $RUN cp -a /etc/resolv.conf $MOUNT_DIR/etc/

  $RUN umount $MOUNT_DIR

  # Start the container
  $RUN lxc-start -n $cname

  # Wait for the container to start
  $RUN lxc-wait -n $cname -s RUNNING

  # disable networking:
  $RUN lxc-attach -n $cname -- sysv-rc-conf --level S networking off

  # restart continer:
  $RUN lxc-stop -n $CONTAINER_NAME
  $RUN lxc-wait -n $CONTAINER_NAME -s STOPPED
  $RUN lxc-start -n $CONTAINER_NAME
  $RUN lxc-wait -n $CONTAINER_NAME -s RUNNING

  # Install NGINX inside the container
  $RUN lxc-attach -n $cname -- apt-get update
  $RUN lxc-attach -n $cname -- apt-get install -y nginx-light php-fpm php-curl php-gd php-intl php-mbstring php-soap php-xml php-xmlrpc php-zip mariadb-server

  $RUN lxc-attach -n $cname -- wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -O /usr/local/bin/wp
  $RUN lxc-attach -n $cname -- chmod +x /usr/local/bin/wp
}
# Need cron?
# apt-get install unattended-upgrades
# dpkg-reconfigure unattended-upgrades # answer 'Yes'
