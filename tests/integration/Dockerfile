FROM 200ms/alpinenet_dev2

ENV FEATURES="python"

PKGS_LVM="lvm2 lvm2-openrc"
PKGS_LXC="lxc  lxc-download lxc-templates"

PKGS_SYS="e2fsprogs xz"
PKGS_DEV="lxc-dev"

PKGS="$PKGS_LVM $PKGS_LXC $PKGS_SYS $PKGS_DEV"

RUN apk add $PKGS

COPY ./files/lvm_lo.start /etc/local.d/


