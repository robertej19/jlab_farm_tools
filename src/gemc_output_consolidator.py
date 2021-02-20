#!/bin/python
#cython: language_level=3


import random 
import sys
import os, subprocess
import argparse
import shutil
from shutil import copyfile

def move_files(args,outdirs):

    dir_list = os.listdir(args.gemcdir)

    print(dir_list)
    print(args.gemcdir)

    lund_filename = 'lund.dat'
    dst_filename = 'dst.hipo'

    files_for_transfer = [dst_filename,]

    for dir in dir_list:
        print("On dir {}".format(dir))
        files = os.listdir(args.gemcdir+dir)
        print(files)
        if args.l:
            if lund_filename in files and dst_filename in files:
                print("Found LUND and DST Files in {}".format(dir))
                files_for_transfer = [dst_filename,lund_filename]
            else:
                print("DST and Lund not found in {}, skipping".format(dir))
                continue
        else:
            if dst_filename in files:
                print("Found DST File in {}".format(dir))
                files_for_transfer = [dst_filename,]
            else:
                continue

        for index,filename in enumerate(files_for_transfer):
            print("Moving {}".format(filename))
            rename = "{}_{}".format(dir,filename)
            copyfile(args.gemcdir+dir+"/"+filename,outdirs[index]+rename)
            print("Moved to {}".format(outdirs[index]+rename))


if __name__ == "__main__":


    #Since __file__ doesn't work when compiled with cython, do the following:
    #From here: https://stackoverflow.com/questions/19630634/python-file-is-not-defined
    #getattr(sys, 'frozen', False)
    #if getattr(sys, 'frozen', False):
    __file__ = os.path.dirname(sys.executable)
    #doesnt work if compiled: exe_abs_path = os.getcwd()+__file__.split(os.path.basename(__file__))[0]+"../../run/gen_processors/"
    exe_abs_path = __file__.split(os.path.basename(__file__))[0]+"run/gen_processors/"

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    default_outdir_base = "/volatile/clas12/robertej/"
    parser.add_argument("--gemcdir",help="Specify full or relative path to gemc output dir",default="/volatile/clas12/osg/robertej/job_2369/output/")
    parser.add_argument("--outdir",help="Specify full or relative path that you want lund/dst files saved to",default=default_outdir_base)
    parser.add_argument("-l",help="Require transferring LUND files",default=False,action='store_true')
    parser.add_argument("-t",help="use for testing on local",default=False,action='store_true')
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')
    args = parser.parse_args()

    if args.t:
        args.gemcdir = "./robertej/osg/job_23232/output/"
        default_outdir_base = "./robertej/"
        args.outdir = default_outdir_base

    if args.outdir == default_outdir_base:
            args.outdir = args.outdir + "gemc_transfer_{}/".format(args.gemcdir.split("/")[-3])

    if not os.path.isdir(args.gemcdir):
        print("\n \n \n------------- ----- ---------------------")
        print("------------- ERROR ---------------------")
        print("------------- ----- ---------------------")
        print("GEMC Output dir: \n \n {} \n \nis not found, specifcy gemc dir path with --gemcdir flag, exiting".format(args.gemcdir))
        sys.exit()

    dst_dir_extension = "dsts/"
    lund_dir_extension = "lunds/"
    dst_outdir = args.outdir + dst_dir_extension
    lund_outdir = args.outdir + lund_dir_extension

    files_to_transf = "dst and lund files" if args.l else "dst files"
    print("Transfering {} from \n {} \n to \n {}".format(files_to_transf,args.gemcdir,args.outdir))
    
    outdirs = [dst_outdir,lund_outdir] if args.l else [dst_outdir,]

    for dirname in outdirs:  
        if not os.path.isdir(dirname):
            print(dirname+" is not present, creating now")
            subprocess.call(['mkdir','-p',dirname])
        else:
            print(dirname + "exists already")
            if args.r:
                print("trying to remove output dir")
                try:
                    shutil.rmtree(dirname)
                except OSError as e:
                    print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                    print("trying to remove dir again")
                    try:
                        shutil.rmtree(dirname)
                    except OSError as e:
                        print ("Error removing dir: %s - %s." % (e.filename, e.strerror))
                        print("WARNING COULD NOT CLEAR OUTPUT DIRECTORY")
                subprocess.call(['mkdir','-p',dirname])

    move_files(args,outdirs)
        


        




