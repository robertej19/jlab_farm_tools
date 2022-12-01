#!/bin/python
#cython: language_level=3


import sys
import os, subprocess
import argparse
import shutil
import subprocess
import os
import time
from datetime import datetime
from datetime import timedelta
start=datetime.now()
time.sleep(1)


def sub_jobs(args):

    if not os.path.isdir(args.jobsdir):
        print("{} directory not found, exiting".format(args.jobsdir))
        sys.exit()
    jobs_list = []
    for f in os.listdir(args.jobsdir):
        f_path = args.jobsdir + f
        if os.path.isfile(f_path):
            jobs_list.append(f)
    jobs_list = sorted(jobs_list)
    print("Found {} files in jobs directory".format(len(jobs_list)))

    if args.n < 1:
        args.n = len(jobs_list) 

    if not os.path.exists(args.jobsdir+"submitted/"):
        os.makedirs(args.jobsdir+"submitted/")

    
    for ind in range(0,args.n):
        file = jobs_list[ind]
        filesub = args.jobsdir + file
        print("\n On file {} of {}".format(ind,args.n))
        print("Trying to submit job {}".format(file))
        
        try:
            process = subprocess.Popen(['sbatch', filesub],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            os.rename(filesub, args.jobsdir +"submitted/"+ file)

            print("Current time: {}".format(datetime.now().strftime("%d-%H.%M.%S")))
            hertz = (ind+1)/(datetime.now()-start).total_seconds()
            seconds_left = (args.n-ind)/hertz
            ETF = datetime.now() + timedelta(seconds=seconds_left)
            print("EFT: {}".format(ETF.strftime("%d-%H.%M.%S")))
        except OSError as e:
            print("Submission failed, error is:")
            print(e)
        


if __name__ == "__main__":
    #Since __file__ doesn't work when compiled with cython, do the following:
    #From here: https://stackoverflow.com/questions/19630634/python-file-is-not-defined
    #getattr(sys, 'frozen', False)
    #if getattr(sys, 'frozen', False):
    __file__ = os.path.dirname(sys.executable)
    jsubs_abs_path = __file__.split(os.path.basename(__file__))[0]+"sub_warehouse/"
    
    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--jobsdir",help="directory containing all jobs txt files to be submitted",default=jsubs_abs_path)
    parser.add_argument("-n",type=int,help="Select number of files to submit (-n 0 will submit all jobs)",default=0)
    args = parser.parse_args()

    sub_jobs(args)