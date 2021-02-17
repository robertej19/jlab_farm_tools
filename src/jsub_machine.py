#!/bin/python
#cython: language_level=3


import random 
import sys
import os, subprocess
import argparse
import shutil

def gen_jsub(args,count):
    outfile = open(args.outdir+"jsub_lund_job_{}.txt".format(count),"w")
    string = """PROJECT: clas12
JOBNAME: pi0gen_{0}

TRACK: analysis
DISK_SPACE: 4 GB

MEMORY: 1024 MB

COMMAND:
cp {14}make_aao_norad_inp.exe .
cp {14}aao_norad.exe . 
cp {14}lundfilt.exe .
./make_aao_norad_inp.exe --physics_model {2} --flag_ehel {3} --npart {4} --epirea {5} --ebeam {6} --q2min {7} --q2max {8} --epmin {9} --epmax {10} --nmax {11} --fmcall {12} --boso {13} --out aao_input_{0}.inp
./aao_norad.exe < aao_input_{0}.inp
./lundfilt.exe -f aao_norad.lund -o post_filter.lund

SINGLE_JOB: true

OUTPUT_DATA:post_filter.lund
OUTPUT_TEMPLATE:{1}pi0_gen{0}.lund
""".format(count,args.d,args.physics_model,args.flag_ehel,args.npart,args.epirea,
    args.ebeam,args.q2min,args.q2max,args.epmin,args.epmax,
    args.nmax,args.fmcall,args.boso,args.exedir)
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

    parser = argparse.ArgumentParser(description="Get args")
    parser.add_argument("--outdir",help="Specify full or relative path to output directory for jsub file",default=exe_abs_path+"../../sub_warehouse/")
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')
    parser.add_argument("-n",type=int,help="Number of submission files",default=1)
    parser.add_argument("-d",type=str,help="Output Dir for Farm Return File",default="/volatile/clas12/robertej/")
    parser.add_argument("--exedir",type=str,help="Specifcy full path of executables directory, otherwise uses default",default=exe_abs_path)
    
    #For make_aao_norad_inp.exe
    parser.add_argument("--physics_model",help="Physics model: 1=A0, 4=MAID98, 5=MAID2000",default=5)
    parser.add_argument("--flag_ehel",help="0= no polarized electron, 1=polarized electron",default=1)
    parser.add_argument("--npart",help="number of particles in BOS banks: 2=(e-,h+), 3=(e-,h+,h0)",default=3)
    parser.add_argument("--epirea",help="final state hadron: 1=pi0, 3=pi+",default=1)
    parser.add_argument("--ebeam",help="incident electron beam energy in GeV",default=10.6)
    parser.add_argument("--q2min",help="minimum Q^2 limit in GeV^2",default=0.2)
    parser.add_argument("--q2max",help="maximum Q^2 limit in GeV^2",default=10.6)
    parser.add_argument("--epmin",help="minimum scattered electron energy limits in GeV",default=0.2)
    parser.add_argument("--epmax",help="maximum scattered electron energy limits in GeV",default=10.6)
    parser.add_argument("--nmax",help="number of output events",default=10000)
    parser.add_argument("--fmcall",help="factor to adjust the maximum cross section, used in M.C. selection",default=1.0)
    parser.add_argument("--boso",help="1=bos output, 0=no bos output",default=1)
    parser.add_argument("--out",help="lund input filename",default="aao_norad_input.inp")
    
    
    args = parser.parse_args()

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
    
    print("Generating {} submission files".format(args.n))
    for index in range(0,args.n):
        print("Creating submission file {} of {}".format(index+1,args.n))
        gen_jsub(args,index)
