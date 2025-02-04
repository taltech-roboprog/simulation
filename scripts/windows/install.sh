#!/bin/bash

# Get the absolute path to the script
SCRIPT_PATH=$(realpath "$0" 2>/dev/null || readlink -f "$0")

# Extract the directory of the script
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

echo "Cleaning old install..."
"$SCRIPT_DIR/uninstall.sh"
echo "Creating symlinks..."
ln -s "$SCRIPT_DIR/robot_test" /usr/bin
if [ $? -ne 0 ]; then
    echo "Run this command from 'Git Bash' in Administrator mode"
else
    ln -s "$SCRIPT_DIR/key_install" /usr/bin
    sed -i "s,INSTALL_DIR_PLACEHOLDER,$(printf '%q' "$SCRIPT_DIR")," /usr/bin/robot_test
    echo "Finished!"
fi
