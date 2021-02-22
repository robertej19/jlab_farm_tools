import os
base = "/mnt/c/Users/rober/Dropbox/Bobby/Linux/work/CLAS12/mit-clas12-analysis/theana/paragon/gen_tools/src"
path = base+"/lunds_renamed/"

files = os.listdir(path)

for file in files:
	filex = file.split(".dat")[0]
	segs = filex.split("_")
	renamed_file = segs[0]+"_"+segs[2]+"_"+segs[1]+".dat"
	os.rename(os.path.join(path,file),os.path.join(path,renamed_file))
