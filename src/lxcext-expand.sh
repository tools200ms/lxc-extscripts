#!/bin/bash

[ -n "$DEBUG" ] && [[ $(echo "$DEBUG" | tr '[:upper:]' '[:lower:]') =~ ^y|yes|1|on$ ]] && \
        set -xe || set -e


function exp_print_help() {
  cat << EOF
$BASE_SCRIPT expand <lxc cont. name> <size>
        expand  - increase container's root fs space
EOF
}

function op_expand() {
  cname=$1
  size_incr=$2

  if [ -z "$cname" ] && ! [[ $size_incr =~ ^[0-9]{1,6}[k|m|g]$ ]]; then
    echo "Provide container name and size by which to increase space"
    exit 1
  fi

  if ! [ $(lxc-ls --stopped --line | grep -Fx cname$) ]; then
    echo "Container: $cname has not been stoped"
    exit 1
  fi

  $RUN lvextend -L "+$size_incr" /dev/mapper/vg1com-$cname
  $RUN e2fsck -f /dev/mapper/$VGNAME-$cname
  $RUN resize2fs /dev/mapper/$VGNAME-$cname
}
