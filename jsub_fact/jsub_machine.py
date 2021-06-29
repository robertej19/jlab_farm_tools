import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import random 
import sys
import os, subprocess

def gen_jsub(count,filename):
    trimmed_name = filename.replace(".hipo","")
    outfile = open("jsub_factory/jsub_job_{}.txt".format(trimmed_name),"w")
    print("generating jsub for {}".format(filename))
    string = """PROJECT: clas12
JOBNAME: dvpipFilter{}

TRACK: analysis
DISK_SPACE: 4 GB

MEMORY: 1024 MB

COMMAND:
cp /work/clas12/robertej/hipo_to_root/convert . 
./convert


INPUT_FILES: 
/work/clas12/robertej/filtered_skim8_files/{}


SINGLE_JOB: true

OUTPUT_DATA:ntuple.root 
OUTPUT_TEMPLATE:/work/clas12/robertej/converted_filtered_skim8/{}.root""".format(count,filename,trimmed_name)
    outfile.write(string)
    outfile.close()



data_dir = "../filtered_skim8_files/"

data_lists = os.listdir(data_dir)

print(data_lists)

for count,file in enumerate(data_lists):
    gen_jsub(count,file)
