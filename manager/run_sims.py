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


def generate_aao_jsub_files(args,params,logging_file):
    executable = args.source_aao_rad_jsub if args.rad else args.source_aao_norad_jsub

    try:
        subprocess.run([executable,
            "--input_exe_path", str(args.input_exe_path_norad),
            "--physics_model", str(args.physics_model),
            "--flag_ehel", str(args.flag_ehel),
            "--npart", str(args.npart),
            "--epirea", str(args.epirea),
            "--ebeam", str(args.ebeam),
            "--q2min", str(args.q2min),
            "--q2max", str(args.q2max),
            "--epmin", str(args.epmin),
            "--epmax", str(args.epmax),
            "--fmcall", str(args.fmcall),
            "--boso", str(args.boso),
            "--trig", str(args.trig),
            "--precision", str(args.precision),
            "--maxloops", str(args.maxloops),
            "--generator_exe_path", str(args.aao_norad_exe_location),
            "--filter_exe_path", str(args.filter_exe_path_norad),
            "--xBmin", str(args.xBmin),
            "--xBmax", str(args.xBmax),
            "--w2min", str(args.w2min),
            "--w2max", str(args.w2max),
            "--tmin", str(args.tmin),
            "--tmax", str(args.tmax),
            "--outdir", str(args.outdir),
            "--seed", str(args.seed),
            "--docker", str(args.docker),
            "--track", str(args.track),
            "--jsub_textdir", params.jsub_generator_dir,
            "-n", str(args.n),
            "--return_dir", params.generator_return_dir,
            "--multi_phase_space",
            "--pi0_gen_exe_path", str(args.pi0_gen_exe_path)])
        logging_file.write("\n\nCreated JSub files at: {}".format(params.jsub_generator_dir))
        return 0
    except OSError as e:
        print("\nError creating generator input file")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        logging_file.write("\n\nEvent Generation Jsubs failed, error message: {}".format(e))
        return -1

def submit_generator_jsubs(args,params,logging_file):
    executable = args.jsubmitter
    try:
        subprocess.run([executable,
            "--jobsdir", jsub_generator_dir])
        logging_file.write("\n\nSubmitted JSub files with return to: {}".format(params.generator_return_dir))
        return 0
    except OSError as e:
        print("\nError creating generator input file")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        logging_file.write("\n\nEvent Generation Jsub batch farm submission failed, error message: {}".format(e))
        return -1

def gemc_submission_details(args,params,logging_file):
    logging_file.write("\n\n On GEMC webportal (https://gemc.jlab.org/web_interface/index.php) Submit the following: \n")
    for mag_field_config in params.mag_field_configs:
        logging_file.write("\n\n Select LUND Files \n")
        logging_file.write("Configuration: rga_fall2018 \n")
        logging_file.write("Magnetic Fields: {} \n".format(mag_field_config))
        logging_file.write("LUND Location: {} \n".format(params.generator_return_dir))
        logging_file.write("Background Merging: No \n")

    logging_file.write("\n\n When GEMC is complete, run the following: \n")
    logging_file.write("python3.6 {}".format(params.output_location+"/copyscript.py"))

    logging_file.write("\n\n When copying files from GEMC is complete, run the following: \n")
    logging_file.write("python3.6 {}".format(params.output_location+"/filter_convert_jsub.py"))

def generate_copy_script(args,params,logging_file):
    logging_file = open(params.output_location+"/copyscript.py", "a")
    logging_file.write("""#!/bin/python3.6m
import subprocess""")
    
    for config in params.configs:
        logging_file.write("""
gemc_return_location = input("Enter full path (e.g. /volatile/.../job_2814/output/) of GEMC output dir for configuration '{}': ")
try:
    print("Copying files from GEMC output to local dir")
    subprocess.run(['python3.6','{}',"-d",gemc_return_location,"-o",'{}'])
except OSError as e:
    print("Error encountered, copying failed")
    print("Error message was:",e.strerror)""".format(config,args.dst_copier_path,params.output_location+"/2_GEMC_DSTs/"+config+"/"))
    
def generate_fc_script(args,params,logging_file):
    logging_file = open(params.output_location+"/filter_convert_jsub.py", "a")
    logging_file.write("""#!/bin/python3.6m
import subprocess""")
    
    for option in ["/Gen/","/Recon/"]:
        converter_exe = args.converter_recon_exe_path if option=="/Recon" else args.converter_gen_exe_path
        for index,config in enumerate(params.configs):
            polarity = params.polarities[index]
            logging_file.write("""
try:
    print("Creating jsub text tiles")
    subprocess.run(['python3.6','{}',
                    "--polarity",'{}',
                    "--outdir",'{}',
                    "--return_dir",'{}',
                    "--hipo_dir",'{}',
                    "--filter_exedir",'{}',
                    "--convert_dir",'{}',
                    "--twophotons"])
    try:
        subprocess.run(['{}',
            "--jobsdir", '{}'])
    except OSError as e:
        print("Error encountered, could not submit fc jsub jobs")
except OSError as e:
    print("Error encountered, fc jsub creation failed")
    print("Error message was:",e.strerror)""".format(args.filt_conv_jsub_path,
                polarity,
                params.output_location+"/0_JSub_Factory/Filter_Convert/"+config+option,
                params.output_location+"/3_Filtered_Converted_Root_Files/"+config+option,
                params.output_location+"/2_GEMC_DSTs/"+config,
                args.filter_exe_path,
                converter_exe,
                args.jsubmitter,
                params.output_location+"/0_JSub_Factory/Filter_Convert/"+config+option))


#         logging_file.write("""
# gemc_return_location = input("Enter full path (e.g. /volatile/.../job_2814/output/) of GEMC output dir for configuration '{}': ")
# try:
#     print("Copying files from GEMC output to local dir")
#     subprocess.run(['python3.6','{}',"-d",gemc_return_location,"-o",'{}'])
# except OSError as e:
#     print("Error encountered, copying failed")
#     print("Error message was:",e.strerror)""".format(config,args.dst_copier_path,params.output_location+"/2_GEMC_DSTs/"+config+"/"))
    
    


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
    main_dir = "/simulations_"+dt_string
    subdirs = ["0_JSub_Factory","1_Generated_Events",
            "2_GEMC_DSTs","3_Filtered_Converted_Root_Files","4_Final_Output_Files"]


        # Jsub file creator for norad generator
    location_of_jsub_factory_aao_rad = main_source_dir + "/aao_gen/gen_wrapper/batch_farm_executables/src/rad/jsub_aao_rad_generator.py"
        # Jsub file creator for rad generator
    location_of_jsub_factory_aao_norad = main_source_dir + "/aao_gen/gen_wrapper/batch_farm_executables/src/norad/jsub_aao_norad_generator.py"
        # Jsub submitting tool
    location_of_jsubmitter = main_source_dir+"/jlab_farm_tools/src/jsubs/jsubmitter.py"
        # aao_(no)rad generator wrapper aka aao_gen
    location_of_aao_gen = main_source_dir+"/aao_gen/gen_wrapper/batch_farm_executables/src/aao_gen.py"
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
        # dst copier path
    location_of_dst_copier = main_source_dir+"/jlab_farm_tools/other-tools/dst_copier_from_gemc_output.py"
        # filter convert jsub machine
    location_of_fc_jsub_machine = main_source_dir + "/jlab_farm_tools/src/jsubs/jsub_filter_convert_machine.py"
        #filter exe path
    location_of_filter_exe = main_source_dir + "/filter/fiducial-filtering/filterEvents/"

    location_of_converter_gen_exe = main_source_dir +  "/convertingHipo/minimal/convertGen"
    location_of_converter_recon_exe = main_source_dir + "/convertingHipo/minimal/convertRec"

    parser = argparse.ArgumentParser(description="""Need to write the description \n
                    This script: \n
                    1.) \n
                    2.) \n
                    3.) """,formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #Directory Structure
    parser.add_argument("--base_dir",help="Location for directory containing all files",default='/volatile/clas12/robertej')
        
        #Executables locations
            #Jsub file creator for norad generator
    parser.add_argument("--source_aao_norad_jsub",help="Location for norad generator jsub creator",default=location_of_jsub_factory_aao_norad)
            #Jsub file creator for rad generator
    parser.add_argument("--source_aao_rad_jsub",help="Location for rad generator jsub creator",default=location_of_jsub_factory_aao_rad)
            #Jsub submitting tool
    parser.add_argument("--jsubmitter",help="Location for jsubmission utility",default=location_of_jsubmitter)
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
            # dst copier path
    parser.add_argument("--dst_copier_path",help="Path to dst copier",default=location_of_dst_copier)
            # Filter & Convert machine jsub path
    parser.add_argument("--filt_conv_jsub_path",help="Location for filt-convert jsub creator",default=location_of_fc_jsub_machine)
                # Filter executable path
    parser.add_argument("--filter_exe_path",help="Location for filter executable path",default=location_of_filter_exe)
                # gen converter executable path
    parser.add_argument("--converter_gen_exe_path",help="Location for converter for gen executable path",default=location_of_converter_gen_exe)
                    #recon converter executable path
    parser.add_argument("--converter_recon_exe_path",help="Location for converter for recon executable path",default=location_of_converter_recon_exe)
    

            #This arguement can be ignored and should be deleted
    parser.add_argument("--outdir",help="Location of intermediate return files between generation and filtering, can be ignored for batch farm",default="output/")

   #File structure:
    # simulations_20210341014_2302
    # ├── 0_Jsub_factory
        # │   ├── Generation
            # │   │   └── jsub_gen_#.txt
        # │   ├── Filtering_Converting
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
    # ├── 4_Final files
        # │   ├── config_1
                # │   │   └── merged_recon.root
                # │   │   └── merged_gen.root
        # │   ├── config_2
            # │   │   └── merged_recon.root
            # │   │   └── merged_gen.root
        # │   ├── config_3
                # │   │   └── merged_recon.root
                # │   │   └── merged_gen.root
    

    #########################################################

    #Specific to creating jsub files
    parser.add_argument("--track",help="jsub track, e.g. debug, analysis",default="analysis")
    parser.add_argument("-n",type=int,help="Number of batch submission text files",default=1)
    parser.add_argument("--multi_phase_space",help="split xbmin-xmax q2min-q2max over smaller phase spaces",default=False,action='store_true')
    parser.add_argument("-s","--submit",help="submit generator jsubs to batch farm",default=False,action='store_true')


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
    mag_field_configs = []
    polarities = []
    if args.f18_in:
        configs.append("Fall_2018_Inbending")
        mag_field_configs.append("tor-1.00_sol-1.00")
        polarities.append("inbending")
    if args.f18_out_100:
        configs.append("Fall_2018_Outbending_100")
        mag_field_configs.append("tor+1.01_sol-1.00")
        polarities.append("outbending")
    if args.f18_out_101:
        configs.append("Fall_2018_Outbending_101")
        mag_field_configs.append("tor+1.00_sol-1.00")
        polarities.append("outbending")




    if len(configs)==0:
        print("\n \n \n Error: No configurations selected. Use flags (-h) to set. Exiting \n \n \n")
        sys.exit()

    if args.test:
        args.base_dir = "/".join(full_file_path.split("/")[:-1])
        print("on local, base dir set to {}".format(args.base_dir))
    output_location = args.base_dir+main_dir


    if not os.path.isdir(args.base_dir):
        print("The base directory {} does not exist, exiting".format(args.base_dir))
        print("Either use the -t flag to test locally, or create the specified base directory")
        print("Use the flag --base_dir to set a different base directory")
        sys.exit()

    if not os.path.isdir(output_location):
        subprocess.call(['mkdir','-p',output_location])
        print("Making main directory at {}".format(output_location))
    else:
        print("Main directory already exists at {}, exiting".format(output_location))
        sys.exit()

    #for config in configs:
    #    print("Creating directory structure for {} configuration run".format(config))
    for directory in subdirs:
        subprocess.call(['mkdir','-p',output_location+"/"+directory])
    for config in configs:
        subprocess.call(['mkdir','-p',output_location+"/0_JSub_Factory/Filter_Convert/"+config+"/Gen"])
        subprocess.call(['mkdir','-p',output_location+"/0_JSub_Factory/Filter_Convert/"+config+"/Recon"])
        subprocess.call(['mkdir','-p',output_location+"/2_GEMC_DSTs/"+config])
        subprocess.call(['mkdir','-p',output_location+"/3_Filtered_Converted_Root_Files/"+config+"/Gen"])
        subprocess.call(['mkdir','-p',output_location+"/3_Filtered_Converted_Root_Files/"+config+"/Recon"])
        subprocess.call(['mkdir','-p',output_location+"/4_Final_Output_Files/"+config])


    jsub_generator_dir = output_location+ "/0_JSub_Factory/Generation/"
    jsub_filter_convert_dir = output_location+ "/0_JSub_Factory/Filtering_Converting/"    
    generator_return_dir  = output_location+ "/1_Generated_Events/"
    filt_conv_return_dir = output_location+ "/3_Filtered_Converted_Root_Files"
    final_dir = output_location+ "/4_Final_Output_Files"

    class parameters:
        def __init__(self,jgd,jfcd,grd,fcrd,fd,configs,mag_field_configs,output_location,polarities):
            self.jsub_generator_dir=jgd
            self.jsub_filter_convert_dir=jfcd
            self.generator_return_dir=grd
            self.filt_conv_return_dir=fcrd
            self.final_dir=fd
            self.mag_field_configs = mag_field_configs
            self.configs = configs
            self.output_location = output_location
            self.polarities = polarities


    

    params = parameters(jsub_generator_dir,
            jsub_filter_convert_dir,
            generator_return_dir,
            filt_conv_return_dir,
            final_dir,configs,
            mag_field_configs,
            output_location,
            polarities)
    
    logging_file = open(output_location+"/readme.txt", "a")
    logging_file.write("Simulation Start Date: {}".format(now))
    


    #########
    # NEED TO INCLUDE SPLITTING MECHANISM OVER PHASE SPACE
    # Generate Lund files
        # Create jsub files for lunds
    generate_aao_jsub_files(args,params,logging_file)
        # Submit the jsub files
    if args.submit:
        submit_generator_jsubs(args,params,logging_file)

    # Submit jobs to GEMC through webportal
    gemc_submission_details(args,params,logging_file)


    # Copy DST files to local directories
        # Generate a sh script to run to copy, and give running insructions
    generate_copy_script(args,params,logging_file)

    # Filter and convert files
        # Generate a sh script to generate and submit jsubs, and give running insructions
    generate_fc_script(args,params,logging_file)

    # Generate emails and send out when various steps are complete
    #generate_root_merger_script(args,params,logging_file)


    logging_file.close()
