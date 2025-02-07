If there are issues with numpy and target architecture on MacOS ('arm' vs 'x86'), try the following:

- close running terminal
- go to Applications/utilities/ in finder, right-click on terminal and select show_info
- select open with Rosetta
- open new terminal window
- uninstall numpy
- reinstall numpy with flags '--compile (--no-cache-dir)'
  - if you also have issues with open ssl certificate add flags '--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org'
  - complete command then: 'pip install --compile --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org numpy'
- close terminal
- go to Applications/utilities, right-click terminal and de-select open with Rosetta
- open new terminal
- run roobt_test...
