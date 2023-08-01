#! /bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "This script requires root, run it with sudo."
    exit 1
fi

set -eux

apt-get update

apt-get install -y --no-install-recommends \
  evince \
  cron \
  wget \
  python3.6
