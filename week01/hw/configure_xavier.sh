#!/bin/sh

# Add user to docker group to avoid sudo
sudo usermod -aG docker $USER

# Create and enable a 32 GB swap space
sudo mkdir /data
sudo fallocate -l 32G /data/swapfile
sudo chmod 600 /data/swapfile
sudo mkswap /data/swapfile
sudo swapon /data/swapfile
sudo swapon -s
echo "/data/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab

