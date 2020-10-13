pdb=${1}

ROSETTABIN=/common/rosetta/rosetta_bin_linux_2018.33.60351_bundle/main/source/bin
ROSETTADB=/common/rosetta/rosetta_bin_linux_2018.33.60351_bundle/main/database/
SUFFIX=.static.linuxgccrelease

$ROSETTABIN/relax${SUFFIX} -s $pdb \
-database $ROSETTADB \
-in:auto_setup_metals \
-use_input_sc \
-constrain_relax_to_start_coords -ignore_unrecognized_res \
-nstruct 6 \
-relax:coord_constrain_sidechains  \
#-relax:cartesian-score:weights ref2015_cart \
-relax:weights ref2015_cart \
-relax:min_type lbfgs_armijo_nonmonotone \
-relax:script cart2.script
