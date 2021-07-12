Simulation Start Date: 2021-07-12 12:25:44.610675 
Invoked with args: ['run_sims.py', '-t', '--f18_in']


Created JSub files at: /mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/0_JSub_Factory/Generation/

 On GEMC webportal (https://gemc.jlab.org/web_interface/index.php) Submit the following: 


 Select LUND Files 
Configuration: rga_fall2018 
Magnetic Fields: tor-1.00_sol-1.00 
LUND Location: /mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/1_Generated_Events/ 
Background Merging: No 


 When GEMC is complete, run the following: 
python3.6 /mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/copyscript.py

 When copying files from GEMC is complete, run the following: 
python3.6 /mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/filter_convert_jsub.py

 When filtering + converting is complete, run the following: 
python3.6 /mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/jlab_farm_tools/manager/simulations_20210712_1225/root_merger_script.py