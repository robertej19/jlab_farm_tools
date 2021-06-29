#!/usr/bin/python3

import random 
import sys
import os, subprocess
import argparse
import shutil

def gen_jsub(args,extra_args,count,filename):

    filename_base = filename.split(".hipo")[0]
    print(filename_base)
    outfile = open(args.outdir+"jsub_filtering_job_{}.txt".format(count),"w")
    string = """PROJECT: clas12
JOBNAME: filtering_converting_{0}

TRACK: {1}
DISK_SPACE: 4 GB

MEMORY: 1024 MB

COMMAND:
mkdir -p bin/
mkdir -p target/
cp {2}bin/filterEvents bin/
cp {2}target/filter-1.2.1.jar target/
cp {11}convertRec .
./bin/filterEvents --start={4} --end={5} --polarity={6} {7} {8}
rm {12}
./convertRec

INPUT_FILES:
{3}

SINGLE_JOB: true

OUTPUT_DATA: recwithgen.root
OUTPUT_TEMPLATE:{10}{9}_filtered_converted.root
""".format(count,args.track,args.filter_exedir,args.hipo_dir+filename,
    args.proc_start,args.proc_end,args.polarity,extra_args,
    filename,filename_base,args.return_dir,args.convert_dir,filename)
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

    
    if not os.path.isdir(args.outdir):
        print(args.outdir+" is not present, creating now")
        subprocess.call(['mkdir','-p',args.outdir])
    else:
        print(args.outdir + "exists already")
        if args.r:
            print("trying to remove output dir")
            try:
                shutil.rmtree(args.outdir)
            except OSError as e:
                print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                print("trying to remove dir again")
                try:
                    shutil.rmtree(args.outdir)
                except OSError as e:
                    print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                    print("WARNING COULD NOT CLEAR OUTPUT DIRECTORY")
            subprocess.call(['mkdir','-p',args.outdir])

    submissions_list = sorted(os.listdir(args.hipo_dir))

    if args.n < 1:
        args.n = len(submissions_list) 

    print("Generating {} submission files".format(args.n))
    for index in range(0,args.n):
        print("Creating submission file {} of {}".format(index+1,args.n))
        gen_jsub(args,extra_args,index,submissions_list[index])
