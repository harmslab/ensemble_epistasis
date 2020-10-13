#!/usr/bin/env python3
__description__ = \
"""
Take output from rosetta that looks like the following:

state,replicate,file,mut1,mut2,score,ddg
apo,struct_0002.pdb,S80C.ddg,None,None,-484.381,None
apo,struct_0002.pdb,S80C.ddg,None,None,-484.373,None
...

and generate all possible mutatn cycles.
"""
__author__ = "Michael J. Harms"
__usage__ = "extract-from-rosetta.py input_csv output_txt"
__date__ = "2020-04-22"


import numpy as np
import pandas as pd

import pickle, sys

def extract_cycles(df,output_txt):
    """
    Create a file containing thermodynamic cycles
    """
    
    # Create set of all mutations seen
    all_muts_seen = []
    genotype_dict = {"apo":{},"ca":{},"ca-pep":{}}
    for i in range(len(df.file)):

        g = (df.iloc[i].mut1,df.iloc[i].mut2)
        state = df.iloc[i].state
        
        all_muts_seen.append(df.iloc[i].mut1)
        all_muts_seen.append(df.iloc[i].mut2)
        try:
            genotype_dict[state][g].append(df.iloc[i].ddg)
        except KeyError:
            genotype_dict[state][g] = [df.iloc[i].ddg]
        
        if i % 5000 == 0:
            print(f"Reading line {i} of {len(df.file)}")
            sys.stdout.flush()
    
    print("Mapping genotype to ddG...")
    sys.stdout.flush()
    
    all_muts_seen = list(set(all_muts_seen))
    all_muts_seen.remove("None")

    # Create dictionary that keys genotype to ddG
    genotype_to_ddg = {}
    for state in genotype_dict.keys():
        genotype_to_ddg[state] = {}

        for g in genotype_dict[state].keys():

            v = np.array([ddg for ddg in genotype_dict[state][g] if ddg != "None"],dtype=np.float)
            if len(v) == 0:
                continue

            m = np.mean(v)
            s = np.std(v)
            genotype_to_ddg[state][g] = (m,s)
    
    print("... done.")
    sys.stdout.flush()
    
    print("Constructing cycles (slow)...")
    sys.stdout.flush()

    f = open(output_txt,"w")       
    fmt_string = "{},{}" + 18*",{:.3f}"  + "\n"   
 
    # Go through all i, j possible mutations
    for i in range(len(all_muts_seen)):
        m1 = all_muts_seen[i]
        site_i = int(m1[1:-1])

        print(f"Mutant {i} of {len(all_muts_seen)}")
        sys.stdout.flush()

        for j in range(i+1,len(all_muts_seen)):
            m2 = all_muts_seen[j]
            site_j = int(m2[1:-1])

            # nonsensical to build mutant cycle for two mutations at the same site
            if site_i == site_j: 
                continue
            
            # Get effects of mutation 1 and 2 on the apo, ca, and cap-pep states.
            # If missing on any one of these states, drop it. 
            try:
                apo_ddG_1 = genotype_to_ddg["apo"][(m1,"None")]
                apo_ddG_2 = genotype_to_ddg["apo"][(m2,"None")]

                ca_ddG_1 = genotype_to_ddg["ca"][(m1,"None")]
                ca_ddG_2 = genotype_to_ddg["ca"][(m2,"None")]

                capep_ddG_1 = genotype_to_ddg["ca-pep"][(m1,"None")]
                capep_ddG_2 = genotype_to_ddg["ca-pep"][(m2,"None")]
            except KeyError:
                continue

            # Try to get double mutant ddGs.  If we can't, this mutation pair
            # must not have been seen together
            
            mut_tuple = (m1,m2)
            try:
                apo_ddG_12 = genotype_to_ddg["apo"][mut_tuple]
                ca_ddG_12 = genotype_to_ddg["ca"][mut_tuple]
                capep_ddG_12 = genotype_to_ddg["ca-pep"][mut_tuple]
    
            except KeyError:
                mut_tuple = (m2,m1)
                try:
                    apo_ddG_12 = genotype_to_ddg["apo"][mut_tuple]
                    ca_ddG_12 = genotype_to_ddg["ca"][mut_tuple]
                    capep_ddG_12 = genotype_to_ddg["ca-pep"][mut_tuple]
                    
                except KeyError:
                    apo_ddG_12 = [np.nan,np.nan]
                    ca_ddG_12 = [np.nan,np.nan]
                    capep_ddG_12 = [np.nan,np.nan]
                    
            f.write(fmt_string.format(mut_tuple[0],
                                      mut_tuple[1],
                                      apo_ddG_1[0],
                                      apo_ddG_2[0],
                                      apo_ddG_12[0],
                                      ca_ddG_1[0],
                                      ca_ddG_2[0],
                                      ca_ddG_12[0],
                                      capep_ddG_1[0],
                                      capep_ddG_2[0],
                                      capep_ddG_12[0],
                                      apo_ddG_1[1],
                                      apo_ddG_2[1],
                                      apo_ddG_12[1],
                                      ca_ddG_1[1],
                                      ca_ddG_2[1],
                                      ca_ddG_12[1],
                                      capep_ddG_1[1],
                                      capep_ddG_2[1],
                                      capep_ddG_12[1]))
            f.flush()


    f.close()

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    try:
        input_csv = argv[0]
        output_txt = argv[1]
    except IndexError:
        err = f"Incorrect arguments. Usage:\n\n{__usage__}\n\n"   
        raise ValueError(err)
     
    # Load csv file with effect of every mutation calculated using Rosetta
    df = pd.read_csv(input_csv,index_col=False)

    # Write out cycles
    extract_cycles(df,output_txt)

if __name__ == "__main__":
    main()
