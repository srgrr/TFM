# Master's Thesis Repository
This repository contains all the LaTeX, images, source codes, experiments, and results from my master's thesis.

This thesis is developed at the Barcelona Supercomputing Center (BSC-CNS) in the Workflows and Distributed Computing group (@bsc-wdc).

## Preliminary observations
All the scripts and programs have been run and tested under Debian-like OS. Some scripts won't work on other OS due to that (e.g: the ones that use specific package managers).

All the COMPSs applications are guaranteed to work only with the used versions during the development phase. Although COMPSs usually has no retrocompatibility issues we think that it is important to leave this warning here.

## LaTeX Document
The LaTeX document can be built as follows:
```
./install_dependencies.sh
./make_tex.sh
```
This will generate a `tfm.pdf` in the root folder.


## COMPSs applications
Most COMPSs applications can be run with `runcompss name_of_main_script`. In case of doubt, the `README` file inside the folder (if any) of the application will prevail.
