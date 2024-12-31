FROM 200ms/alpinenet_dev2

ENV FEATURES="python"

ENV PKGS_LVM="lvm2 lvm2-openrc"
ENV PKGS_LXC="lxc  lxc-download lxc-templates"

ENV PKGS_SYS="e2fsprogs xz"
ENV PKGS_DEV="lxc-dev"

ENV PKGS="$PKGS_LVM $PKGS_LXC $PKGS_SYS $PKGS_DEV"


RUN apk add $PKGS
COPY ./files/lvm_lo.start /etc/local.d/


