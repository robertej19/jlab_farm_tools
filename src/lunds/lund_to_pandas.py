#!/bin/python3.4
#cython: language_level=3

import pandas as pd
import argparse
import sys
import os



lund_header_labels =["num_particles",
"target_mass",
"target_atom_num",
"target_pol",
"beam_pol",
"beam_type",
"beam_energy",
"interaction_nuc_id",
"process_id",
"event_weight"]

lund_particle_labels = ["sub_index",
    "lifetime",
    "type_1active",
    "particleID",
    "ind_parent",
    "ind_daughter",
    "mom_x",
    "mom_y",
    "mom_z",
    "E_GeV",
    "Mass_GeV",
    "Vx",
    "Vy",
    "Vz"]


def convert_lund_file_to_df(filename):
    print("Converting file {}".format(filename))
    events = []
    event_ind = -1
    with open(filename,"r") as f:
        for line in f:
            line_str = str(line)
            if line_str[1] is not ' ': #LUND format has the number of particles in the second character of a header
                event_ind += 1
                #print("header")
                values = [event_ind,]
                events.append([])
                
                cols = line.split()  
                for ind, val in enumerate(cols):
                    values.append(float(val))
                #print(values)
                events[event_ind].append(values)
            
                #print(events)
                ###Write to header
            else:
                values = []
                #print("particle content")
                cols = line.split()
                for ind, val in enumerate(cols):
                    values.append(float(val))
                events[event_ind].append(values)
    events_repacked = []
    for event in events:
        for particle_ind in range(1,len(event)):
            events_repacked.append(event[0]+event[particle_ind])    


    df_labels = ["event_num"]+lund_header_labels+lund_particle_labels
    df = pd.DataFrame(events_repacked, columns=df_labels)
    
    return df


if __name__ == "__main__":

    #Since __file__ doesn't work when compiled with cython, do the following:
    #From here: https://stackoverflow.com/questions/19630634/python-file-is-not-defined
    #getattr(sys, 'frozen', False)
    #if getattr(sys, 'frozen', False):
    #__file__ = os.path.dirname(sys.executable)
    #doesnt work if compiled: exe_abs_path = os.getcwd()+__file__.split(os.path.basename(__file__))[0]+"../../run/gen_processors/"
    #exe_abs_path = __file__.split(os.path.basename(__file__))[0]+"run/gen_processors/"

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    default_lund_inname = "lund_simu_998.dat"
    default_pandas_outname = ".pkl"
    parser.add_argument("-i","--infile",help="Specify lund input filename",default=default_lund_inname)
    parser.add_argument("-o","--outfile",help="Specify pandas outupt filename",default=default_pandas_outname)
    args = parser.parse_args()

    if not os.path.isfile(args.infile):
        print("Cannot find file {}, exiting".format(args.infile))
        sys.exit()

    if args.outfile == default_pandas_outname:
        args.outfile = args.infile.split(".")[0]+args.outfile
    

    df = convert_lund_file_to_df(args.infile)  
    print(df)

    df.to_pickle(args.outfile)
    
    print("Saved pkl file to {}\n".format(args.outfile))

