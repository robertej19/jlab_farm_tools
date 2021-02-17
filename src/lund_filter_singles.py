#!/bin/python
#cython: language_level=3

import os
import argparse

def vec_subtract(vec1,vec2):
    res = tuple(map(lambda i, j: i - j, vec1, vec2)) 
    return res

def vec_add(vec1,vec2):
    res = tuple(map(lambda i, j: i + j, vec1, vec2)) 
    return res

def calc_inv_mass_squared(four_vector):
    fv = four_vector
    inv_mass2 = fv[0]**2-fv[1]**2-fv[2]**2-fv[3]**2
    return inv_mass2

e_mass = 0.000511
Ebeam_4mom = (10.6,0,0,10.6)
p_mass = 0.938

def filter_lund(infile_name,output_filename):
    with open(infile_name,"r") as lst:
        txtlst = lst.readlines()

    outlines = []
    for ind,line in enumerate(txtlst):
        if ind %5000 == 0:
            print("On event {}".format(ind/5))

        if ind % 5 == 0:
            a = line
            b = txtlst[ind+1]
            c = txtlst[ind+2]
            d = txtlst[ind+3]
            e = txtlst[ind+4]
            for sub_line in (a,b,c,d):
                cols = sub_line.split()
                if cols[3]=='11':
                    e_4mom = (float(cols[9]),float(cols[6]),float(cols[7]),float(cols[8]))
                    Q2 = -1*calc_inv_mass_squared(vec_subtract(Ebeam_4mom,e_4mom))
                    W2 = calc_inv_mass_squared(vec_subtract(vec_add(Ebeam_4mom,(p_mass,0,0,0)),e_4mom))
                    if Q2>1 and W2>3.61:
                        outlines.append(a)
                        outlines.append(b)
                        outlines.append(c)
                        outlines.append(d)
                        outlines.append(e)
                        
              
    print("Original length {}, filtered length {}".format(len(txtlst)/5,len(outlines)/5))
    print(output_filename)
    with open(output_filename, 'w') as f:
        f.write(''.join(outlines))


datadir = "original_lunds/"
outdir = "filtered_lunds/"
#lund_filenames = os.listdir(datadir)

parser = argparse.ArgumentParser(description="Get args")
parser.add_argument("-f",help="filename")
parser.add_argument("-o",help='output')
args = parser.parse_args()

lund_filename = args.f
output_filename = args.o

#for ind,lund_filename in enumerate(lund_filenames):
print("trying to process file {}".format(lund_filename))
#print("On file {} out of {}".format(ind+1,len(lund_filenames)))
filter_lund(lund_filename,output_filename)
