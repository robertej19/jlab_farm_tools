#!/bin/python
#cython: language_level=3

import os
import argparse

"Consult aao_norad generator repository README for options descriptions"

def gen_input(args):
    outfile = open(args.out,"w")
    print("generating aao_norad_input file named {}".format(args.out))
    string = """{}
{}
{}
{}
{}
{} {}
{} {}
{}
{}
{}
""".format(args.physics_model,args.flag_ehel,args.npart,args.epirea,
    args.ebeam,args.q2min,args.q2max,args.epmin,args.epmax,
    args.nmax,args.fmcall,args.boso)
    outfile.write(string)
    outfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get args")
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
    parser.add_argument("--out",help="output filename",default="aao_norad_input.inp")
    args = parser.parse_args()

    gen_input(args)
