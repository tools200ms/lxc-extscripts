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

  if [ -n $(lxc-info -n $cname -s | grep -e 'STOPPED$') ]; then
    $RUN lxc-stop -n $cname
    $RUN lxc-wait -n $cname -s STOPPED
  else
    echo "Container already stopped"
  fi

  MOUNT_DIR=/mnt/lxc/$cname
  dev_path="/dev/mapper/$VGNAME-"$(echo $cname | sed "s/-/--/g")

  $RUN mkdir -p $MOUNT_DIR
  $RUN mount $dev_path $MOUNT_DIR
}

function op_umounts() {
  cname=$1

  MOUNT_DIR=/mnt/lxc/$cname

  $RUN umount $MOUNT_DIR
  $RUN rmdir $MOUNT_DIR

  $RUN lxc-start -n $cname
}

