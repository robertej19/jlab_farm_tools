#!/bin/python3.6m
import subprocess
try:
    print("Running root merger for",'Fall_2018_Inbending','gen')
    subprocess.run(['python3.6','/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/root_combiner.py',
                    "-d",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/3_Filtered_Converted_Root_Files/Fall_2018_Inbending/Gen/',
                    "-o",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/4_Final_Output_Files/Fall_2018_Inbending/merged_Fall_2018_Inbending_gen.root'])
except OSError as e:
    print("Error encountered, fc jsub creation failed")
    print("Error message was:",e.strerror)
try:
    print("Running root merger for",'Fall_2018_Inbending','recon')
    subprocess.run(['python3.6','/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/root_combiner.py',
                    "-d",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/3_Filtered_Converted_Root_Files/Fall_2018_Inbending/Recon/',
                    "-o",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/4_Final_Output_Files/Fall_2018_Inbending/merged_Fall_2018_Inbending_recon.root'])
except OSError as e:
    print("Error encountered, fc jsub creation failed")
    print("Error message was:",e.strerror)