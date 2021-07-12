#!/bin/python3.6m
import subprocess
try:
    print("Creating jsub text tiles")
    subprocess.run(['python3.6','/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/src/jsubs/jsub_filter_convert_machine.py',
                    "--polarity",'inbending',
                    "--outdir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/0_JSub_Factory/Filter_Convert/Fall_2018_Inbending/Gen/',
                    "--return_dir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/3_Filtered_Converted_Root_Files/Fall_2018_Inbending/Gen/',
                    "--hipo_dir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/2_GEMC_DSTs/Fall_2018_Inbending/',
                    "--filter_exedir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/filter/fiducial-filtering/filterEvents/',
                    "--convert_dir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/convertingHipo/minimal/convertGen',
                    "--convert_type",'gen',
                    "--twophotons"])
    try:
        subprocess.run(['/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/src/jsubs/jsubmitter.py',
            "--jobsdir", '/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/0_JSub_Factory/Filter_Convert/Fall_2018_Inbending/Gen/'])
    except OSError as e:
        print("Error encountered, could not submit fc jsub jobs")
except OSError as e:
    print("Error encountered, fc jsub creation failed")
    print("Error message was:",e.strerror)
try:
    print("Creating jsub text tiles")
    subprocess.run(['python3.6','/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/src/jsubs/jsub_filter_convert_machine.py',
                    "--polarity",'inbending',
                    "--outdir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/0_JSub_Factory/Filter_Convert/Fall_2018_Inbending/Recon/',
                    "--return_dir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/3_Filtered_Converted_Root_Files/Fall_2018_Inbending/Recon/',
                    "--hipo_dir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/2_GEMC_DSTs/Fall_2018_Inbending/',
                    "--filter_exedir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/filter/fiducial-filtering/filterEvents/',
                    "--convert_dir",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/convertingHipo/minimal/convertRec',
                    "--convert_type",'recon',
                    "--twophotons"])
    try:
        subprocess.run(['/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/src/jsubs/jsubmitter.py',
            "--jobsdir", '/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/0_JSub_Factory/Filter_Convert/Fall_2018_Inbending/Recon/'])
    except OSError as e:
        print("Error encountered, could not submit fc jsub jobs")
except OSError as e:
    print("Error encountered, fc jsub creation failed")
    print("Error message was:",e.strerror)