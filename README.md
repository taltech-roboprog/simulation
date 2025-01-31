# Simulator (Webots)

## Installation

1. Install the simulator according to the instructions at [https://cyberbotics.com](https://cyberbotics.com/#download)
   * NB! Please use all default settings if installing on Windows (or you have to make manual changes to files later)
2. Install Git if not installed
   * **Windows:** ["Git for Windows"](https://git-scm.com/downloads/win)
   * **Debian:** Use `apt install git`
   * **MacOS:** Use `brew install git`. If homebrew is not currently installed, then run `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`, then install git using the previous command.
3. Clone this repository
   * **Windows:**
     * Open a "Git Bash shell" by pushing the Windows key and writing "git bash"
     * Execute `git clone https://github.com/taltech-roboprog/simulation` in the shell
     * Close the shell by executing `exit`
   * **Debian:**
     * Execute `git clone https://github.com/taltech-roboprog/simulation` in the shell
   * **MacOS:**
     * Execute `git clone https://github.com/taltech-roboprog/simulation` in the shell
4. Install the testing script `robot_test`
   * **Windows:**
     * Open an Administrator "Git Bash shell" by pushing the Windows key and writing "git bash" and right-click on the search result and select "Run as Administrator"
     * Execute `simulation/scripts/windows/install.sh`
     * Close the shell by executing `exit`
   * **Debian:** Execute `simulation/scripts/debian/install.sh`
   * **MacOS:**  
     * cd to `simulation/scripts/mac/` folder in terminal
     * Execute `chmod +x *` to give execute permissions
     * Execute `./install.sh`
5. Congratulations! Now you can run the robot testing script `robot_test` in the shell.
