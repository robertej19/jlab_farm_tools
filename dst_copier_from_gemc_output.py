import os
from shutil import copyfile

#data_dir = "gemc_output/"
data_dir = "/volatile/clas12/osg/robertej/job_2369/output/"
#dst_out_dir = 'gemc_copied/dsts/'
#lund_out_dir = 'gemc_copied/lunds/'
#lund_out_dir = '/work/clas12/robertej/gemc20210211copied/lunds/'
dst_out_dir = '/work/clas12/robertej/gemc20210214_copied/dsts/'

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
