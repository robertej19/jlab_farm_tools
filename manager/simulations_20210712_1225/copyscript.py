#!/bin/python3.6m
import subprocess

user = input("Enter username, e.g. robertej: " )

gemc_job_number = input("Enter GEMC job number (e.g. 3163) of GEMC output dir for configuration 'Fall_2018_Inbending': ")
gemc_return_location = "/volatile/clas12/osg2/{}/job_{}/output/".format(user,gemc_job_number)
try:
    print("Copying files from GEMC output at {} to local dir".format(gemc_return_location))
    subprocess.run(['python3.6','/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/other-tools/dst_copier_from_gemc_output.py',"-d",gemc_return_location,"-o",'/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/2_GEMC_DSTs/Fall_2018_Inbending/'])
    logging_file = open('/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/readme.txt',"a")
    logging_file.write("GEMC Directory for configuration {} is {}".format(Fall_2018_Inbending,gemc_return_location))
except OSError as e:
    print("Error encountered, copying failed")
    print("Error message was:",e.strerror)