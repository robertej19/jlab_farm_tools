# pi0_gen_tools
# Usage:

git clone https://github.com/robertej19/pi0_gen_tools.git
cd pi0_gen_tools/
chmod +x run/* run/gen_processors/*

#To get help messages and see all avaliable flags:
./run/make_jsubs.exe -h
./run/submit_jsubs.exe -h

#Example of how make jsubmission text files for aao_norad generator:
./run/make_jsubs.exe -r -n 10 --q2min 0.99 --ebeam 10.6 --nmax 150000 -d /volatile/clas12/robertej/
This will generate 10 submissions scripts in a default directory named "sub_warehouse" to generate 150,000 events which will be filtered to have Q2>1 W2>4 and return files to /volatile/clas12/robertej

#Now submit the jobs to batch farm:
./run/submit_jsubs.exe 
#Since we did not include any flags, this will process all jsub submission scripts from the default directory

#Check here to see status of jobs on batch farm:
https://scicomp.jlab.org/scicomp/index.html#/farmJobs/activeJob

#How to transfer output files from GEMC to a different directory
./run/gemc_copier.exe --gemcdir=/volatile/clas12/osg/robertej/job_2408/output/ --outdir=/volatile/clas12/robertej/testpi0sim1K/ -l  
As always, use ./run/gemc_copier.exe -h to see a full list of options
