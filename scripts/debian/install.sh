#!/bin/bash

# Get the absolute path to the script
SCRIPT_PATH=$(realpath "$0" 2>/dev/null || readlink -f "$0")

# Extract the directory of the script
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

echo "Cleaning old install..."
$SCRIPT_DIR/uninstall.sh
echo "Creating symlinks..."
sudo ln -s $SCRIPT_DIR/robot_test /usr/local/bin
sudo ln -s $SCRIPT_DIR/stop_robot /usr/local/bin
sudo ln -s $SCRIPT_DIR/key_install /usr/local/bin
echo "Finished!"
