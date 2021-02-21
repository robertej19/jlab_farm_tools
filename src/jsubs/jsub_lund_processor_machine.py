#!/bin/python
#cython: language_level=3

import random 
import sys
import os, subprocess
import argparse
import shutil

def gen_jsub(args,count,filename):

    filename_base = filename.split(".")[0]
    print(filename_base)
    outfile = open(args.jsub_dir+"jsub_lund_processing_job_{}.txt".format(count),"w")
    string = """PROJECT: clas12
JOBNAME: lund_processing_{0}

TRACK: {1}
DISK_SPACE: 4 GB

MEMORY: 1024 MB

COMMAND:
cp {2}lund_to_pandas.exe .
cp {2}process_lund_events.exe .
./lund_to_pandas.exe -i {4} -o {5}
./process_lund_events.exe -i {5} -o {6}

INPUT_FILES:
{3}

SINGLE_JOB: true

OUTPUT_DATA: {6}
OUTPUT_TEMPLATE:{7}{6}
""".format(count,args.track,args.exe_dir,args.lund_dir+filename,
    filename,filename_base+".pkl",filename_base+"_evented.pkl",
    args.return_dir)
    outfile.write(string)
    outfile.close()

if __name__ == "__main__":
    #Since __file__ doesn't work when compiled with cython, do the following:
    #From here: https://stackoverflow.com/questions/19630634/python-file-is-not-defined
    #getattr(sys, 'frozen', False)
    #if getattr(sys, 'frozen', False):
    __file__ = os.path.dirname(sys.executable)
    #doesnt work if compiled: exe_abs_path = os.getcwd()+__file__.split(os.path.basename(__file__))[0]+"../../run/gen_processors/"
    exe_abs_path = __file__.split(os.path.basename(__file__))[0]+"run/gen_processors/"

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')
    parser.add_argument("-n",type=int,help="Number of submission files",default=0)
    parser.add_argument("--lund_dir",type=str,help="Specifcy full path of lund directory, otherwise uses default",default=exe_abs_path+"../../../hipotest/")
    parser.add_argument("--jsub_dir",help="Specify full or relative path to output directory for jsub file",default=exe_abs_path+"../../sub_lund_proc_warehouse/")

    #For filter options
    parser.add_argument("--exe_dir",type=str,help="Specifcy full path of executables directory, otherwise uses default",default=exe_abs_path)
    parser.add_argument("--return_dir",type=str,help="Output Dir for Farm Return File",default="/volatile/clas12/robertej/")
    parser.add_argument("--track",help="jsub track, e.g. debug, analysis",default="analysis")

    args = parser.parse_args()

    
    if not os.path.isdir(args.lund_dir):
        print("\n \n \n------------- ----- ---------------------")
        print("------------- ERROR ---------------------")
        print("------------- ----- ---------------------")
        print("Lund dir: \n \n {} \n \nis not found, specifcy lund dir path with --lund_dir flag, exiting".format(args.lund_dir))
        sys.exit()

    
    if not os.path.isdir(args.jsub_dir):
        print(args.jsub_dir+" is not present, creating now")
        subprocess.call(['mkdir','-p',args.jsub_dir])
    else:
        print(args.jsub_dir + "exists already")
        if args.r:
            print("trying to remove output dir")
            try:
                shutil.rmtree(args.jsub_dir)
            except OSError as e:
                print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                print("trying to remove dir again")
                try:
                    shutil.rmtree(args.jsub_dir)
                except OSError as e:
                    print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                    print("WARNING COULD NOT CLEAR OUTPUT DIRECTORY")
            subprocess.call(['mkdir','-p',args.jsub_dir])

    submissions_list = sorted(os.listdir(args.lund_dir))

    if args.n < 1:
        args.n = len(submissions_list) 

    print("Generating {} submission files".format(args.n))
    for index in range(0,args.n):
        print("Creating submission file {} of {}".format(index+1,args.n))
        gen_jsub(args,index,submissions_list[index])
