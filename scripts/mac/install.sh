#!/bin/bash

# path
SCRIPT_PATH=$(readlink -f "$0" 2>/dev/null || perl -MCwd -e 'print Cwd::abs_path shift' "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

echo "Cleaning old install..."
"$SCRIPT_DIR/uninstall.sh"
echo "Creating symlinks..."

# symlinking
sudo ln -s "$SCRIPT_DIR/robot_test" /usr/local/bin
sudo ln -s "$SCRIPT_DIR/stop_robot" /usr/local/bin
sudo ln -s "$SCRIPT_DIR/key_install" /usr/local/bin
echo "Finished!"
