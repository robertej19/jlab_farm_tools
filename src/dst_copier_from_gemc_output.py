import os
from shutil import copyfile

import argparse

#if __name__ == "__main__":
    
parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument("-i","--infile", help="input file", default="input.txt")
parser.add_argument("-d","--datadir", help="input directory", default="/volatile/clas12/osg2/robertej/job_2814/output/")
parser.add_argument("-o","--outdir", help="output directory", default="/volatile/clas12/robertej/lowerxbqt_return/")


args = parser.parse_args()

print(args)

data_dir = args.datadir
dst_out_dir = args.outdir

#data_dir = "gemc_output/"
#data_dir = "/volatile/clas12/osg/robertej/job_2369/output/"
#data_dir = "/volatile/clas12/osg/robertej/job_2532/output/"
#dst_out_dir = 'gemc_copied/dsts/'
#lund_out_dir = 'gemc_copied/lunds/'
#lund_out_dir = '/work/clas12/robertej/gemc20210211copied/lunds/'
#dst_out_dir = '/work/clas12/robertej/gemc20210214_copied/dsts/'
#dst_out_dir = '/volatile/clas12/robertej/10kjob_dsts_20210326/'

lund_filename = 'lund.dat'
dst_filename = 'dst.hipo'

dir_list = os.listdir(data_dir)

for dir in dir_list:
	print("On dir {}".format(dir))
	files = os.listdir(data_dir+dir)
	if dst_filename in files:
		#lund_outname = "{}lund_{}.dat".format(lund_out_dir,dir)
		dst_outname = "{}dst_{}.hipo".format(dst_out_dir,dir)
		#copyfile(data_dir+dir+"/"+lund_filename,lund_outname)
		copyfile(data_dir+dir+"/"+dst_filename,dst_outname)
