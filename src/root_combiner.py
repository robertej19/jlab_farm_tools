from os import listdir
from os.path import isfile, join
import argparse
import sys
import os, subprocess


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Get args",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    

    parser.add_argument("-d","--root_dir",help="directory containing root files",default="root_files/")
    parser.add_argument("-o","--output_path",help="output file location and name",default="none")
    
    args = parser.parse_args()

    if not os.path.isdir(args.root_dir):
        print(args.root_dir+" cannot be found, exiting")
        sys.exit()

    mypath = args.root_dir

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print("found {} files in {}, writing macro file to combine them".format(len(onlyfiles),args.root_dir))

    outfile = open("combine_macro.C","w")
    string_start = r"""{
        TChain ch("T");
        """

    string_middle = ""

    for file_name in onlyfiles:
        string_middle += """ch.Add("{}{}");
        """.format(args.root_dir,file_name)

    if args.output_path == "none":
        string_end = """ch.Merge("merged_{}_files.root");
        """.format(len(onlyfiles))
    else:
        string_end = """ch.Merge("{}");
        """.format(args.output_path)
    
    string_end_bracket = r"""
}"""
    outfile.write(string_start+string_middle+string_end+string_end_bracket)
    outfile.close()

    print("finished making macro file, now executing in root")
    try:
        subprocess.run(["root","-q","combine_macro.C"])
    except OSError as e:
        print("\nError processing root macro")
        print("The error message was:\n %s - %s." % (e.filename, e.strerror))
        print("Exiting\n")
        sys.exit()
    
    print("Merging complete, merged is at {}".format(args.output_path))