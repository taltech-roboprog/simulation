If there are issues with numpy and target architecture on MacOS (`arm` vs `x86`), try the following:

- close running terminal
- go to `Applications/utilities/` in finder, right-click on terminal and select `Get Info`
- select `Open with Rosetta`
- open new terminal window
- uninstall numpy
- to reinstall numpy with flags `--compile --no-cache-dir` run `pip install --compile --no-cache-dir numpy`
  - if you also have issues with open ssl certificate add flags `--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org` to allow sources
  - complete command then: `pip install --compile --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org numpy`
- close terminal
- go to `Applications/utilities`, right-click terminal, select `Get Info` and de-select `Open with Rosetta`
- open new terminal
- run roobt_test...
