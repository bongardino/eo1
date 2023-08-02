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
  python3.6 \
  kmscube \
  libxcb-dri3-dev \
  x11proto-dri3-dev \
  unclutter
  # curl \
  # kmscube \

# TODO: gradually change in cron, ie $ sudo tee /sys/class/backlight/acpi_video0/brightness <<< 6
# backlight control
nano /sys/class/backlight/backlight-pwm1/brightness
