#!/usr/bin/python3

import random 
import sys
import os, subprocess
import argparse
import shutil

## #Multijob example
# PROJECT: clas12
# JOBNAME: filtering_converting_0
# TRACK: debug
# DISK_SPACE: 4 GB
# MEMORY: 1024 MB
# COMMAND:
# mkdir -p bin/
# mkdir -p target/
# cp /w/hallb-scifs17exp/clas12/robertej/analysis_tools/production/filter/fiducial-filtering/filterEvents/bin/filterEvents bin/
# cp /w/hallb-scifs17exp/clas12/robertej/analysis_tools/production/filter/fiducial-filtering/filterEvents/target/filter-1.2.1.jar target/
# cp /w/hallb-scifs17exp/clas12/robertej/analysis_tools/production/convertingHipo/minimal/convertGen ./converter
# ./bin/filterEvents --start=0% --end=100% --polarity=inbending  --twophotons  infile_0.hipo
# rm infile_0.hipo
# ./converter
# INPUT_FILES:
# /volatile/clas12/robertej/simulations_20210707_1232/2_GEMC_DSTs/Fall_2018_Inbending/dst_simu_0.hipo
# /volatile/clas12/robertej/simulations_20210707_1232/2_GEMC_DSTs/Fall_2018_Inbending/dst_simu_1.hipo
# INPUT_DATA: infile_0.hipo
# OUTPUT_DATA: genOnly.root
# OUTPUT_TEMPLATE:/volatile/clas12/robertej/*.root


def gen_jsub(args,extra_args,file_sub_string):

    output_name = "recwithgen.root" if args.convert_type =="recon" else "genOnly.root"
    outfile = open(args.outdir+"jsub_filtering_job_{}.txt".format(args.convert_type),"w")


header = """#!/bin/bash
#
#SBATCH --account=clas12
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=1000
#SBATCH --job-name={2}_{3}.job
#SBATCH --time=24:00:00
#SBATCH --gres=disk:10000
#SBATCH --output={0}sbatch_output/{1}.out
#SBATCH --error={0}sbatch_err/{1}.err

cd /scratch/slurm/$SLURM_JOB_ID

echo "currently located in:"
echo $PWD

# Sleep a random amount of time from 0-180s
# This avoids conflicts when lots of jobs start simultaneously.
TSLEEP=$[ ( $RANDOM % (180+1) ) ]s
echo "Sleeping for ${{TSLEEP}} ..."
sleep $TSLEEP""".format(args.return_dir,
                        file_sub_string.split(".")[0],
                        args.convert_type,
                        args.slurm_job_name)

    string = """
cp {0} ./converter
cp {3} .
./converter
mv {2} {1}FC_Files/{4}_filt_conv.root

""".format( args.convert_dir, 
    args.return_dir,
    output_name, 
    full_file_path, 
    file_sub_string.split(".")[0])  
    outfile.write(header+string)
    outfile.close()



if __name__ == "__main__":
    #Since __file__ doesn't work when compiled with cython, do the following:
    #From here: https://stackoverflow.com/questions/19630634/python-file-is-not-defined
    #getattr(sys, 'frozen', False)
    #if getattr(sys, 'frozen', False):
    __file__ = os.path.dirname(sys.executable)
    exe_abs_path = os.getcwd()+__file__.split(os.path.basename(__file__))[0]+"../../run/gen_processors/"
    #exe_abs_path = __file__.split(os.path.basename(__file__))[0]+"run/gen_processors/"

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')
    parser.add_argument("-n",type=int,help="Number of submission files",default=0)
    parser.add_argument("--outdir",help="Specify full or relative path to output directory for jsub file",default=exe_abs_path+"../../sub_filt_con_warehouse/")
    parser.add_argument("--filter_exedir",type=str,help="Specifcy full path of executables directory, otherwise uses default",default=exe_abs_path)
    parser.add_argument("--track",help="jsub track, e.g. debug, analysis",default="analysis")
    parser.add_argument("--return_dir",type=str,help="Output Dir for Farm Return File",default="/volatile/clas12/robertej/")
    parser.add_argument("--hipo_dir",type=str,help="Specifcy full path of hipo directory, otherwise uses default",default=exe_abs_path+"../../../hipotest/")
    parser.add_argument("--convert_dir",help="specify full path of executible used to convert output into root file",default=exe_abs_path)
    parser.add_argument("--convert_type",help="recon | gen - use to specify if using recon or gen",default="recon")
    parser.add_argument("--slurm_job_name",help="identification name for use in scicomp",default="generic_name_here")

    #For filter options
    parser.add_argument("--proc_end",type=str,help="last event count, or percentage",default="100%")
    parser.add_argument("--proc_start",type=str,help="starting event count, or percentage",default="0%")
    parser.add_argument("--polarity",type=str,help="inbending | outbending",default="inbending")
    parser.add_argument("--twophotons",help="if on, requires two photons in event",default=False,action='store_true')
    parser.add_argument("--eb",help="If on, use eb pid only",default=False,action='store_true')
    args = parser.parse_args()

    
    if not os.path.isdir(args.hipo_dir):
        print("\n \n \n------------- ----- ---------------------")
        print("------------- ERROR ---------------------")
        print("------------- ----- ---------------------")
        print("Hipo dir: \n \n {} \n \nis not found, specifcy hipo dir path with --hipo_dir flag, exiting".format(args.hipo_dir))
        sys.exit()

    extra_args = ""
    if args.twophotons:
        extra_args += " --twophotons "
    if args.eb:
        extra_args += "--eb"

    
    # # # if not os.path.isdir(args.outdir):
    # # #     print(args.outdir+" is not present, creating now")
    # # #     subprocess.call(['mkdir','-p',args.outdir])
    # # # else:
    # # #     print(args.outdir + "exists already")
    # # #     if args.r:
    # # #         print("trying to remove output dir")
    # # #         try:
    # # #             shutil.rmtree(args.outdir)
    # # #         except OSError as e:
    # # #             print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
    # # #             print("trying to remove dir again")
    # # #             try:
    # # #                 shutil.rmtree(args.outdir)
    # # #             except OSError as e:
    # # #                 print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
    # # #                 print("WARNING COULD NOT CLEAR OUTPUT DIRECTORY")
    # # #         subprocess.call(['mkdir','-p',args.outdir])

    submissions_list = sorted(os.listdir(args.hipo_dir))

    
    if args.n < 1:
        args.n = len(submissions_list) 

    file_sub_string = ""
    print("Generating submission file for {} hipo files".format(args.n))
    for index in range(0,args.n):
        file_sub_string += args.hipo_dir+submissions_list[index] +"\n"

    gen_jsub(args,extra_args,file_sub_string)
