#!/bin/python3.6m
#cython: language_level=3
# -*- coding: utf-8 -*-

import random 
import sys
import os, subprocess
import argparse
import shutil
import time
from datetime import datetime 

"""
This is a wrapper for the aao_norad (and aao_rad?) DVPi0 generators. It takes as input command line arguements which 
you can observe with the command line arguement -h, and gives as output a single .dat output file,
in lund format (https://gemc.jlab.org/gemc/html/documentation/generator/lund.html)

Requirements for inclusion on clas12-mcgen: (check requirements at https://github.com/JeffersonLab/clas12-mcgen)
--done-- C++ and Fortran: software should compile using gcc > 8.
--done-- An executable with the same name as the github repository name, installed at the top level dir
--done-- The generator output file name must be the same name as the exectuable + ".dat". For example, the output of clasdis must be clasdis.dat
--done-- If --seed is ignored, the generator is responsible for choosing unique random seeds (without preserving state between jobs), which could be done from a millisecond or better precision system clock.
--done-- The argument --seed <integer value> is added on the OSG to all executable. This option must be ignored or it can be used by the executable to set the generator random seed using <integer value>
--done-- To specify the number of events, the option "--trig" must be used
--done-- The argument --docker is added on the OSG to all executable. This option must be ignored or it can be used by the executable to set conditions to run on the OSG container

To verify all requirements are met, the executable must pass the following test:

genName --trig 10 --docker --seed 1448577483

This should produce a file genName.dat.
"""


def generate_aao_jsub_files(args):
    executable = args.source_aao_rad_jsub if args.rad else args.source_aao_norad_jsub

    try:
        subprocess.run([executable,
            "--input_exe_path", str(args.),
            "--physics_model", str(args.),
            "--flag_ehel", str(args.),
            "--npart", str(args.),
            "--epirea", str(args.),
            "--ebeam", str(args.),
            "--q2min", str(args.),
            "--q2max", str(args.),
            "--epmin", str(args.),
            "--epmax", str(args.),
            "--fmcall", str(args.),
            "--boso", str(args.),
            "--trig", str(args.),
            "--precision", str(args.),
            "--maxloops", str(args.),
            "--generator_exe_path", str(args.),
            "--filter_exe_path", str(args.),
            "--xBmin", str(args.),
            "--xBmax", str(args.),
            "--w2min", str(args.),
            "--w2max", str(args.),
            "--tmin", str(args.),
            "--tmax", str(args.),
            "--outdir", str(args.),
            "-r", str(args.),
            "--seed", str(args.),
            "--docker", str(args.),
            "--track", str(args.),
            "--jsub_textdir", str(args.),
            "-n", str(args.),
            "--return_dir", str(args.),
            "--pi0_gen_exe_path", str(args.)])
        return 0
    except OSError as e:
        print("\nError creating generator input file")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        return -1



if __name__ == "__main__":
    # The following is needed since an executable does not have __file__ defined, but when working in interpreted mode,
    # __file__ is needed to specify the relative file path of other packages. In principle strict relative 
    # path usage should be sufficient, but it is easier to debug / more robust if absolute.
    try:
        __file__
    except NameError:
        full_file_path = sys.executable #This sets the path for compiled python
    else:
        full_file_path = os.path.abspath(__file__) #This sets the path for interpreted python

    main_source_dir = "/".join(full_file_path.split("/")[:-3])

    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M_%s")
    main_dir = "simulations_"+dt_string
    subdirs = ["0_Batch_Farm_Submissions","1_Generated_Events",
            "2_GEMC_DSTs","3_Filtered_Converted_Root_Files","4_Final_Output_Files"]


        # Jsub file creator for norad generator
    location_of_jsub_factory_aao_rad = main_source_dir + "/aao_gen/gen_wrapper/batch_farm_executables/src/rad/jsub_aao_rad_generator.py"
        # Jsub file creator for rad generator
    location_of_jsub_factory_aao_norad = main_source_dir + "/aao_gen/gen_wrapper/batch_farm_executables/src/norad/jsub_aao_norad_generator.py"
        # Jsub submitting tool
    location_of_jsubmitter = main_source_dir+"jlab_farm_tools/src/jsubs/jsubmitter.py"
        # aao_(no)rad generator wrapper aka aao_gen
    location_of_aao_gen = main_source_dir+"/aao_gen/gen_wrapper/batch_farm_executables/aao_gen.py"
        # actual generator location: aao_norad
    location_of_aao_norad = main_source_dir+"/aao_gen/aao_norad/build/aao_norad.exe"
        # actual generator location: aao_rad
    location_of_aao_rad = main_source_dir+"/aao_gen/aao_rad/build/aao_rad.exe"
        # input file maker: aao_norad
    location_of_input_file_maker_aao_norad = main_source_dir+"/aao_gen/gen_wrapper/batch_farm_executables/src/norad/input_file_maker_aao_norad.py"
        # input file maker: aao_rad
    location_of_input_file_maker_aao_rad = main_source_dir+"/aao_gen/gen_wrapper/batch_farm_executables/src/rad/input_file_maker_aao_rad.py"
        # filter path for aao_norad
    location_of_event_filter_aao_norad = main_source_dir+"/aao_gen/gen_wrapper/batch_farm_executables/src/norad/lund_filter_norad.py"
        # filter path for aao_rad
    location_of_event_filter_aao_rad = main_source_dir+"/aao_gen/gen_wrapper/batch_farm_executables/src/rad/lund_filter_rad.py"



    parser = argparse.ArgumentParser(description="""Need to write the description \n
                    This script: \n
                    1.) \n
                    2.) \n
                    3.) """,formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #Directory Structure
    parser.add_argument("--base_dir",help="Location for directory containing all files",default='/volatile/clas12/robertej/')
        
        #Executables locations
            #Jsub file creator for norad generator
    parser.add_argument("--source_aao_norad_jsub",help="Location for norad generator jsub creator",default=location_of_jsub_factory_aao_norad)
            #Jsub file creator for rad generator
    parser.add_argument("--source_aao_rad_jsub",help="Location for rad generator jsub creator",default=location_of_jsub_factory_aao_rad)
            #Jsub submitting tool
    XXXXXXX put in location of jsubmitter
            # aao_(no)rad generator wrapper aka aao_gen
    parser.add_argument("--pi0_gen_exe_path",help="Path to lund filter executable",default=location_of_aao_gen)

            # actual generator location: aao_norad
    parser.add_argument("--aao_norad_exe_location",help="Path to generator executable",default=location_of_aao_norad)
            # actual generator location: aao_rad
    parser.add_argument("--aao_rad_exe_location",help="Path to generator executable",default=location_of_aao_rad)
            # input file maker: aao_norad
    parser.add_argument("--input_exe_path_norad",help="Path to input file maker executable for aao_norad",default=location_of_input_file_maker_aao_norad)
            # input file maker: aao_radrad
    parser.add_argument("--input_exe_path_rad",help="Path to input file maker executable for aao_rad",default=location_of_input_file_maker_aao_rad)
            # filter path for aao_norad
    parser.add_argument("--filter_exe_path_norad",help="Path to lund filter executable",default=location_of_event_filter_aao_norad)
            # filter path for aao_rad
    parser.add_argument("--filter_exe_path_rad",help="Path to lund filter executable",default=location_of_event_filter_aao_rad)

            #This arguement can be ignored and should be deleted
    parser.add_argument("--outdir",help="Location of intermediate return files between generation and filtering, can be ignored for batch farm",default="output/")


    main_dir = "simulations_"+dt_string
    subdirs = ["0_JSub_Factory","1_Generated_Events",
            "2_GEMC_DSTs","3_Filtered_Converted_Root_Files","4_Final_Output_Files"]


   #File structure:
    # simulations_20210341014_2302
    # ├── 0_Jsub_factory
        # │   ├── generation
            # │   │   └── jsub_gen_#.txt
        # │   ├── filtering_converting
            # │   ├── config_1
                # │   │   ├── filt_conv_recon
                    # │   │   └── jsub_fc_config_#_recon_#.txt
                # │   │   ├── filt_conv_gen
                    # │   │   └── jsub_fc_config_#_recon_#.txt
            # │   ├── config_2
                # │   │   ├── filt_conv_recon
                    # │   │   └── jsub_fc_config_#_recon_#.txt
                # │   │   ├── filt_conv_gen
                    # │   │   └── jsub_fc_config_#_recon_#.txt
            # │   ├── config_3
                # │   │   ├── filt_conv_recon
                    # │   │   └── jsub_fc_config_#_recon_#.txt
                # │   │   ├── filt_conv_gen
                    # │   │   └── jsub_fc_config_#_recon_#.txt
    # ├── 1_Lund files
        # └── xbmin_qtmin_#_norad.lund
    # ├── 2_GEMC DSTs
        # │   ├── config_1
            # │   │   └── dst_#.hipo
        # │   ├── config_2
            # │   │   └── dst_#.hipo
        # │   ├── config_3
        # │   │   └── dst_#.hipo
    # ├── 3_Filtered & Converted root files
        # │   ├── config_1
            # │   │   ├── filt_conv_recon root files
                # │   │   │   └── dst_fc_config_#_fc_recon_#.root
            # │   │   ├── filt_conv_recon root files
                # │   │   │   └── dst_fc_config_#__gen_#.root
        # │   ├── config_2
            # │   │   ├── filt_conv_recon root files
                # │   │   │   └── dst_fc_config_#_fc_recon_#.root
            # │   │   ├── filt_conv_recon root files
                # │   │   │   └── dst_fc_config_#__gen_#.root
        # │   ├── config_3
            # │   │   ├── filt_conv_recon root files
                # │   │   │   └── dst_fc_config_#_fc_recon_#.root
            # │   │   ├── filt_conv_recon root files
                # │   │   │   └── dst_fc_config_#__gen_#.root
    # ├── 5_Final files
        # │   ├── config_1
                # │   │   └── merged_recon.root
                # │   │   └── merged_gen.root
        # │   ├── config_2
            # │   │   └── merged_recon.root
            # │   │   └── merged_gen.root
        # │   ├── config_3
                # │   │   └── merged_recon.root
                # │   │   └── merged_gen.root



    #Location of return files on local server:
    parser.add_argument("--jsub_generator_dir",help="Directory containing jsub generation scripts",default=xxxxx "/submission_warehouse/")
    parser.add_argument("--jsub_filter_convert_dir",help="Directory containing jsub filtering converting scripts",default=xxxxx "/submission_warehouse/")


    parser.add_argument("--return_dir",type=str,help="Directory you want batch farm files returned to",default="/volatile/clas12/robertej/")



    #########################################################

    #Specific to creating jsub files
    parser.add_argument("--track",help="jsub track, e.g. debug, analysis",default="analysis")
    parser.add_argument("-n",type=int,help="Number of batch submission text files",default=1)
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')


    #Options for generator and generated event filtering
    parser.add_argument("--physics_model",help="Physics model: 1=A0, 4=MAID98, 5=MAID2000",default=5)
    parser.add_argument("--flag_ehel",help="0= no polarized electron, 1=polarized electron",default=1)
    parser.add_argument("--npart",help="number of particles in BOS banks: 2=(e-,h+), 3=(e-,h+,h0)",default=3)
    parser.add_argument("--epirea",help="final state hadron: 1=pi0, 3=pi+",default=1)
    parser.add_argument("--ebeam",help="incident electron beam energy in GeV",default=10.6)
    parser.add_argument("--q2min",help="minimum Q^2 limit in GeV^2",default=0.2)
    parser.add_argument("--q2max",help="maximum Q^2 limit in GeV^2",default=10.6)
    parser.add_argument("--epmin",help="minimum scattered electron energy limits in GeV",default=0.2)
    parser.add_argument("--epmax",help="maximum scattered electron energy limits in GeV",default=10.6)
    parser.add_argument("--fmcall",help="factor to adjust the maximum cross section, used in M.C. selection",default=1.0)
    parser.add_argument("--boso",help="1=bos output, 0=no bos output",default=1)
    parser.add_argument("--trig",type=int,help="number of generated events",default=10000)
    parser.add_argument("--precision",type=float,help="Enter how close, in percent, you want the number of filtered events to be relative to desired events",default=10)
    parser.add_argument("--maxloops",type=int,help="Enter the number of generation iteration loops permitted to converge to desired number of events",default=10)
    parser.add_argument("--seed",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default="none")
    parser.add_argument("--docker",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default="none")
    parser.add_argument("--xBmin",type=float,help='minimum Bjorken X value',default=-1)
    parser.add_argument("--xBmax",type=float,help='maximum Bjorken X value',default=10)
    parser.add_argument("--w2min",type=float,help='minimum w2 value, in GeV^2',default=-1)
    parser.add_argument("--w2max",type=float,help='maximum w2 value, in GeV^2',default=100)
    parser.add_argument("--tmin",type=float,help='minimum t value, in GeV^2',default=-1)
    parser.add_argument("--tmax",type=float,help='maximum t value, in GeV^2',default=100)


    ##################################

    #General options    
    parser.add_argument("--test","-t",help="Use to test on local environment",default=False,action='store_true')
    parser.add_argument("--rad",help="Use if want to use aao_rad",default=False,action='store_true')
    parser.add_argument("--f18_in",help="Configuration: Fall 2018 Inbending (Torus = -1.00)",default=False,action='store_true')
    parser.add_argument("--f18_out_100",help="Configuration: Fall 2018 Outbending (Torus = +1.00)",default=False,action='store_true')
    parser.add_argument("--f18_out_101",help="Configuration: Fall 2018 Outbending (Torus = +1.01)",default=False,action='store_true')
    args = parser.parse_args()
    
    configs = []
    if args.f18_in:
        configs.append("Fall_2018_Inbending")
    if args.f18_out_100:
        configs.append("Fall_2018_Outbending_100")
    if args.f18_out_101:
        configs.append("Fall_2018_Outbending_101")

    if len(configs)==0:
        print("\n \n \n Error: No configurations selected. Use flags (-h) to set. Exiting \n \n \n")
        sys.exit()

    if args.test:
        args.base_dir = "/".join(full_file_path.split("/")[:-1])
        print("on local, base dir set to {}".format(args.base_dir))

    if not os.path.isdir(args.base_dir):
        print("The base directory {} does not exist, exiting".format(args.base_dir))
        print("Either use the -t flag to test locally, or create the specified base directory")
        print("Use the flag --base_dir to set a different base directory")
        sys.exit()

    if not os.path.isdir(args.base_dir+main_dir):
        subprocess.call(['mkdir','-p',args.base_dir+main_dir])
        print("Making main directory at {}".format(args.base_dir+main_dir))
    else:
        print("Main directory already exists at {}, exiting".format(args.base_dir+main_dir))
        sys.exit()

    #for config in configs:
    #    print("Creating directory structure for {} configuration run".format(config))
    for directory in subdirs:
        subprocess.call(['mkdir','-p',args.base_dir+main_dir+"/"+directory])


    readme_location = args.base_dir+main_dir+"/readme.txt"
    logging_file = open(readme_location, "a")
    logging_file.write("Simulation Start Date: {}".format(now))
    

    
    # Generate Lund files
        # Create jsub files for lunds
        # Submit the jsub files
    generate_aao_jsub_files(args)

    # Submit jobs to GEMC through webportal
        # Give instructions

    # Copy DST files to local directories
        # Generate a sh script to run to copy, and give running insructions

    # Filter and convert files
        # Generate a sh script to generate and submit jsubs, and give running insructions

    # Generate emails and send out when various steps are complete
    


    logging_file.close()

    sys.exit()
    #File structure:
    # repository head
    # ├── aao_norad
    # │   ├── build
    # │   │   └── aao_norad.exe
    # ├── aao_rad
    # ├── gen_wrapper
    # │   ├── run
    # │   │   ├── input_file_maker_aao_norad.exe
    # │   │   └── lund_filter.exe
    # │   └── src
    # │       ├── aao_norad_text.py
    # │       ├── input_file_maker_aao_norad.py
    # │       ├── lund_filter.py
    # │       └── pi0_gen_wrapper.py

    slash = "/"
    #repo_base_dir = slash.join(full_file_path.split(slash)[:-1])
    repo_base_dir = slash.join(full_file_path.split(slash)[:-4])
    output_file_path = repo_base_dir + "/output/"

    norad_input_file_maker_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/norad/input_file_maker_aao_norad.py"
    rad_input_file_maker_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/rad/input_file_maker_aao_rad.py"

    norad_lund_filter_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/norad/lund_filter_norad.py"
    rad_lund_filter_path = repo_base_dir + "/gen_wrapper/batch_farm_executables/src/rad/lund_filter_rad.py"


    aao_norad_path = repo_base_dir + "/aao_norad/build/aao_norad.exe"
    aao_rad_path = repo_base_dir + "/aao_rad/build/aao_rad.exe"



    parser = argparse.ArgumentParser(description="""CURRENTLY ONLY WORKS WITH AAO_NORAD 4 PARTICLE FINAL STATE \n
                                This script: \n
                                1.) Creates an input file for aao_norad \n
                                2.) Generates specified number of events \n
                                3.) Filters generated events based off specifications \n
                                4.) Returns .dat data file""",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
    #General options
    parser.add_argument("--rad",help="Uses radiative generator instead of nonradiative one, CURRENTLY NOT WORKING",default=False,action='store_true')

    #For step 1: input_file_maker_aao_norad
    parser.add_argument("--input_exe_path",help="Path to input file maker executable",default=norad_input_file_maker_path)
    parser.add_argument("--physics_model",help="Physics model: 1=A0, 4=MAID98, 5=MAID2000",default=5)
    parser.add_argument("--flag_ehel",help="0= no polarized electron, 1=polarized electron",default=1)
    parser.add_argument("--npart",help="number of particles in BOS banks: 2=(e-,h+), 3=(e-,h+,h0)",default=3)
    parser.add_argument("--epirea",help="final state hadron: 1=pi0, 3=pi+",default=1)
    parser.add_argument("--ebeam",help="incident electron beam energy in GeV",default=10.6)
    parser.add_argument("--q2min",help="minimum Q^2 limit in GeV^2",default=0.2)
    parser.add_argument("--q2max",help="maximum Q^2 limit in GeV^2",default=10.6)
    parser.add_argument("--epmin",help="minimum scattered electron energy limits in GeV",default=0.2)
    parser.add_argument("--epmax",help="maximum scattered electron energy limits in GeV",default=10.6)
    parser.add_argument("--fmcall",help="factor to adjust the maximum cross section, used in M.C. selection",default=1.0)
    parser.add_argument("--boso",help="1=bos output, 0=no bos output",default=1)
    parser.add_argument("--seed",help="0= use unix timestamp from machine time to generate seed, otherwise use given value as seed",default=0)
    parser.add_argument("--trig",type=int,help="number of generated events",default=10000)
    parser.add_argument("--precision",type=float,help="Enter how close, in percent, you want the number of filtered events to be relative to desired events",default=5)
    parser.add_argument("--maxloops",type=int,help="Enter the number of generation iteration loops permitted to converge to desired number of events",default=10)
    parser.add_argument("--input_filename",help="filename for aao_norad",default="aao_norad_input.inp")


    #Arguements specific to aao_rad
    parser.add_argument("--int_region",help="the sizes of the integration regions",default =".20 .12 .20 .20")
    parser.add_argument("--err_max",help="limit on the error in (mm)**2",default=0.2)
    parser.add_argument("--target_len",help="target cell length (cm)",default=5)
    parser.add_argument("--target_rad",help="target cell cylinder radius",default=0.43)
    parser.add_argument("--cord_x",help="x-coord of beam position",default=0.0)
    parser.add_argument("--cord_y",help="y-coord of beam position",default=0.0)
    parser.add_argument("--cord_z",help="z-coord of beam position",default=0.0)
    parser.add_argument("--rad_emin",help="minimum photon energy for integration",default=0.005)
    parser.add_argument("--sigr_max_mult",help="a multiplication factor for sigr_max",default=0.0)
    parser.add_argument("--sigr_max",help="sigr_max",default=0.005)



    #For step2: (optional) set path to aao_norad generator
    parser.add_argument("--generator_exe_path",help="Path to generator executable",default=aao_norad_path)

    #For step3: (optional) set path to lund filter script and get filtering arguemnets
    parser.add_argument("--xBmin",type=float,help='minimum Bjorken X value',default=-1)
    parser.add_argument("--xBmax",type=float,help='maximum Bjorken X value',default=10)
    parser.add_argument("--w2min",type=float,help='minimum w2 value, in GeV^2',default=-1)
    parser.add_argument("--w2max",type=float,help='maximum w2 value, in GeV^2',default=100)
    parser.add_argument("--tmin",type=float,help='minimum t value, in GeV^2',default=-1)
    parser.add_argument("--tmax",type=float,help='maximum t value, in GeV^2',default=100)
    parser.add_argument("--filter_infile",help="specify input lund file name. Currently only works for 4-particle final state DVPiP",default="aao_norad.lund")
    parser.add_argument("--filter_outfile",help='specify processed lund output file name',default="aao_gen.dat")
   
    #Specify output directory for lund file
    parser.add_argument("--filter_exe_path",help="Path to lund filter executable",default=norad_lund_filter_path)
    parser.add_argument("--outdir",help="Specify full or relative path to output directory final lund file",default=output_file_path)
    parser.add_argument("-r",help="Removes all files from output directory, if any existed",default=False,action='store_true')

    #For conforming with clas12-mcgen standards
    parser.add_argument("--docker",help="this arguement is ignored, but needed for inclusion in clas12-mcgen",default=False,action='store_true')


    if args.rad:
        if args.generator_exe_path==aao_norad_path:
            args.generator_exe_path = aao_rad_path #change to using radiative generator
        if args.filter_infile == "aao_norad.lund":
            args.filter_infile = "aao_rad.lund" #change to using radiative generator
        if args.input_exe_path == norad_input_file_maker_path:
            args.input_exe_path = rad_input_file_maker_path
        if args.input_filename == "aao_norad_input.inp":
            args.input_filename = "aao_rad_input.inp" #change to using radiative generator
        if args.filter_exe_path == norad_lund_filter_path:
            args.filter_exe_path = rad_lund_filter_path
        args.npart = 4 #for now, mandatory switch


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
    
    print("Generating {} DVPiP Events".format(args.trig))
    gen_events(args,repo_base_dir)