#!/bin/bash

[ -n "$DEBUG" ] && [[ $(echo "$DEBUG" | tr '[:upper:]' '[:lower:]') =~ ^y|yes|1|on$ ]] && \
        set -xe || set -e


function mnt_print_help() {
  cat << EOF
$BASE_SCRIPT smount|umounts <lxc cont. name>
        smount  - stop container and mount its root fs
        umounts - umount continer's root fs and start it
EOF
}

function op_smount() {
  cname=$1

  $RUN lxc-stop -n $cname
  $RUN lxc-wait -n $cname -s STOPPED

  $RUN mkdir -p /mnt/lxc/$cname
  $RUN mount /dev/mapper/vg1com-$cname /mnt/lxc/$cname

  MOUNT_DIR=/mnt/lxc/$cname
  $RUN mkdir -p $MOUNT_DIR
  $RUN mount /dev/mapper/$VGNAME-$CONTAINER_NAME $MOUNT_DIR
}

function op_umounts() {
  cname=$1

  MOUNT_DIR=/mnt/lxc/$cname

  $RUN umount $MOUNT_DIR
  $RUN rmdir $MOUNT_DIR

  $RUN lxc-start -n $cname
}
