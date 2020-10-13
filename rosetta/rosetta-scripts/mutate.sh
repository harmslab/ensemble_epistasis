pdb="${1}"
mutfile="${2}"

SUFFIX=.linuxgccrelease

# mut_file same syntax with what being used in ddg-monomer application.
# iterations can be flexible; 3 is fast and reasonable
# dump_pdbs you can save mutants pdb if you want
# bbnbr bb dof, suggestion: i-1, i, i+1
# fa_max_dist: modify fa_atr and fa_sol behavior, really important for protein stability (default: 6)  
cartesian_ddg${SUFFIX} \
 -database $ROSETTA3_DB \
 -s ${pdb} \
 -in:auto_setup_metals \
 -ddg:mut_file ${mutfile} \
 -ddg:iterations 3 \
 -ddg::cartesian \
 -ddg:dump_pdbs false \
 -ddg:bbnbr 1 \
 -fa_max_dis 9.0 \
 -score:weights talaris2014_cart
 -mut_only
# -[scorefunction option]: any other options for score function containing cart_bonded term, for example, -beta_cart or -score:weights talaris2014_cart]
