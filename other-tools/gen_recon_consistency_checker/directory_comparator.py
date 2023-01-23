#get two directories and compare them
#usage: python directory_comparator.py <dir1> <dir2>
#output: a file called "dir1_dir2_comparison.txt" with the list of files that are in dir1 but not in dir2
#        and a file called "dir2_dir1_comparison.txt" with the list of files that are in dir2 but not in dir1
#        and a file called "dir1_dir2_common.txt" with the list of files that are in both dir1 and dir2
#        and a file called "dir1_dir2_common.txt" with the list of files that are in both dir1 and dir2
#        and a file called "dir1_dir2_common.txt" with the list of files that are in both dir1 and dir2
#        and a file called "dir1_dir2_common.txt" with the list of files that are in both dir1 and dir2

# # # import sys
# # # import os
# # # import subprocess
# # # import shutil
# # # import time
# # # from datetime import datetime
# # # import json
# # # import numpy as np
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # import matplotlib as mpl
# # # import argparse
# # # import itertools
# # # import uproot

# # # def get_file_list(directory):
# # #     file_list = []
# # #     for root, dirs, files in os.walk(directory):
# # #         for file in files:
# # #             if file.endswith(".root"):
# # #                 file_list.append(os.path.join(root, file))
# # #     return file_list

# # # def compare_directories(dir1, dir2):
# # #     dir1_files = get_file_list(dir1)
# # #     dir2_files = get_file_list(dir2)
# # #     dir1_dir2_comparison = []
# # #     dir2_dir1_comparison = []
# # #     dir1_dir2_common = []
# # #     dir2_dir1_common = []
# # #     for file in dir1_files:
# # #         if file not in dir2_files:
# # #             dir1_dir2_comparison.append(file)
# # #         else:
# # #             dir1_dir2_common.append(file)
# # #     for file in dir2_files:
# # #         if file not in dir1_files:
# # #             dir2_dir1_comparison.append(file)
# # #         else:
# # #             dir2_dir1_common.append(file)
# # #     return dir1_dir2_comparison, dir2_dir1_comparison, dir1_dir2_common, dir2_dir1_common

# # # in_dir_1_not_dir_2, in_dir_2_not_dir_1, _, _ = compare_directories(sys.argv[1], sys.argv[2])

# # # print("Files in directory 1 but not in directory 2:")
# # # for file in in_dir_1_not_dir_2:
# # #     print(file)

# # # print("Files in directory 2 but not in directory 1:")
# # # for file in in_dir_2_not_dir_1:
# # #     print(file)


import os

# Set the paths for the two directories
dir1 = 'gen/'
dir2 = 'recon/'

# Get the list of files in each directory
files1 = set(os.listdir(dir1))
files2 = set(os.listdir(dir2))

# Find the files that are only in one directory
only_in_dir1 = files1.difference(files2)
only_in_dir2 = files2.difference(files1)

# Print the results
print("Files only in", dir1)
for file in only_in_dir1:
    print(file)

print("\nFiles only in", dir2)
for file in only_in_dir2:
    print(file)

# now remove the uncommon files
for file in only_in_dir1:
    os.remove(dir1+file)

for file in only_in_dir2:
    os.remove(dir2+file)