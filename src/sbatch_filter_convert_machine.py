#!/usr/bin/python3

import random 
import sys
import os, subprocess
import argparse
import shutil

## #Multijob example

    # #!/bin/bash
    # #
    # #SBATCH --account=clas12
    # #SBATCH --nodes=1
    # #SBATCH --ntasks=1
    # #SBATCH --mem-per-cpu=2500
    # #SBATCH --job-name=testrun
    # #SBATCH --time=24:00:00
    # #SBATCH --gres=disk:10000
    # #SBATCH --output=/volatile/clas12/robertej/test.out
    # #SBATCH --error=/volatile/clas12/robertej/test.err
    # #

    # # Sleep a random amount of time from 0-180s
    # # This avoids conflicts when lots of jobs start simultaneously.
    # TSLEEP=$[ ( $RANDOM % (180+1) ) ]s
    # echo "Sleeping for ${TSLEEP} ..."
    # sleep $TSLEEP

    # pwd


def gen_jsub(index,args,extra_args,file_sub_string,full_file_path):

    output_name = "recwithgen.root" if args.convert_type =="recon" else "genOnly.root"
    if args.real_data:
        output_name = "pi0.root"
    outfile = open(args.outdir+"sbatch_filt_conv_{}_{}.txt".format(args.convert_type,index),"w")
    string = """#!/bin/bash
#
#SBATCH --account=clas12
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2500
#SBATCH --job-name={0}_{10}.job
#SBATCH --time=24:00:00
#SBATCH --gres=disk:10000
#SBATCH --output=/volatile/clas12/robertej/{0}.out
#SBATCH --error=/volatile/clas12/robertej/{0}.err
#SBATCH --chdir=/scratch/robertej/
#

# Sleep a random amount of time from 0-180s
# This avoids conflicts when lots of jobs start simultaneously.
TSLEEP=$[ ( $RANDOM % (180+1) ) ]s
echo "Sleeping for ${{TSLEEP}} ..."
sleep $TSLEEP

mkdir -p bin/
mkdir -p target/
cp {1}bin/filterEvents bin/
cp {1}target/filter-1.3.jar target/
cp {2} ./converter
cp {11} .
./bin/filterEvents --start={3} --end={4} --polarity={5} {6} {10}
rm {10}
./converter
mv {8} {7}{12}_filt_conv.root

""".format(args.convert_type,
    args.filter_exedir,
    args.convert_dir,
    args.proc_start,
    args.proc_end,
    args.polarity,
    extra_args,
    args.return_dir,
    output_name,
    args.slurm_job_name,
    file_sub_string,
    full_file_path,
    file_sub_string.split(".")[0])
    outfile.write(string)
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
    parser.add_argument("--real_data",help="use if analyzing real data",default=False,action='store_true')
    parser.add_argument("--test",help="use if on dev machine",default=False,action='store_true')



    #For filter options
    parser.add_argument("--proc_end",type=str,help="last event count, or percentage",default="100%")
    parser.add_argument("--proc_start",type=str,help="starting event count, or percentage",default="0%")
    parser.add_argument("--polarity",type=str,help="inbending | outbending",default="inbending")
    parser.add_argument("--twophotons",help="if on, requires two photons in event",default=False,action='store_true')
    parser.add_argument("--eb",help="If on, use eb pid only",default=False,action='store_true')
    args = parser.parse_args()

    print(args.test)

    if (not args.test) and (not os.path.isdir(args.hipo_dir)):
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
        #file_sub_string += args.hipo_dir+submissions_list[index] +"\n"
        file_sub_string = submissions_list[index]
        full_file_path = args.hipo_dir+file_sub_string
        gen_jsub(index,args,extra_args,file_sub_string,full_file_path)
