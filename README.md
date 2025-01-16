# Simulator (Webots)

## Installation

1. Install the simulator according to the instructions at [https://cyberbotics.com](https://cyberbotics.com/#download)
2. Install Git if not installed
   * **Windows:** ["Git for Windows"](https://git-scm.com/downloads/win)
   * **Debian:** Use `apt install git`
3. Clone this repository
   * **Windows:**
     * Open a "Git Bash shell" by pushing the Windows key and writing "git bash"
     * Execute `git clone https://github.com/taltech-roboprog/simulation` in the shell
     * Close the shell by executing `exit`
   * **Debian:**
     * Execute `git clone https://github.com/taltech-roboprog/simulation` in the shell
4. Install the testing script `robot_test`
   * **Windows:**
     * Open an Administrator "Git Bash shell" by pushing the Windows key and writing "git bash" and right-click on the search result and select "Run as Administrator"
     * Execute `simulation/scripts/windows/install.sh`
   * **Debian:** Execute `simulation/scripts/debian/install.sh`
5. Congratulations! Now you can run the robot testing script `robot_test` in the shell.
