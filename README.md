# Ensemble Epistasis

This repository contains scripts and jupyter notebooks used for the analysis presented in [Ensemble epistasis: thermodynamic origins of non-addivity between mutations]() by Anneliese J. Morrison, Daria R. Wonderlick, and Michael J. Harms. There are three jupyter notebooks (`Figure2.ipynb`, `Figure3.ipynb`,  and `Figure4.ipynb`), corresponding to the display figures in the manuscript. The `rosetta` directory contains the ROSETTTA `ddG` calculations needed for figure 4. 

### ROSETTA calculations

ROSETTA calculations were run using linux build 2018.33.60351.  python scripts were run using python 3.7.3.  Scripts use `pandas` and `numpy` as dependencies. 

+ `00_initial-structures/`: cleaned up and standardized sturctures for the `apo`, `ca`, and `ca-pep` states. 
+ `01_relaxed-structures/`: relaxed structures fed into the `ddG` calculation.  These were relaxed using the `rosetta/rosetta-scripts/relax-structure.sh` script.
+ `02_mut-files/`: ROSETTA-formatted files for introducing the point mutants.  The mut files for each state ( `apo`, `ca`, and `ca-pep`) are stored in individual .zip files. 
+ `03_ddg-results/`: ROSETTA output for ddG of each mutant.  The results for each state ( `apo`, `ca`, and `ca-pep`) are stored in individual .zip files. These were generated using the `rosetta/rosetta-scripts/mutate.sh` script.  The `extract.py` script was used to extract thes reuslts into `ddg-summary.csv`. 
+ `04_cycles/`: script for calculating thermodynamic cycles from mutants.  Script takes a couple of hours to run and dumps out a large file.  This file is `output-cycles.txt` as read in by `Figure4.ipynb`.  To generate, navigate into the `04_cycles` directory and run: `python extract-from-rosetta.py ../03_ddg-results/ddg-summary.csv`.   

This repo does not contain the cluster-specific bash scripts we used to loop over structure/mut-file combinations to run `mutate.sh`.  