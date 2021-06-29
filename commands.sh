#To filter all lund files in a specific dir
#./run/make_lund_jsubs.exe --exe_dir /work/clas12/robertej/tools/pi0_gen_tools/run/lund_processors/ --lund_dir /volatile/clas12/robertej/testpi0sim1K/lunds/ --return_dir /volatile/clas12/robertej/testpi0sim1K/lunds_kin_calc/ --track debug -n 2 -r

#To create and filter various lund files
./run/make_aao_gens.exe --exedir /work/clas12/robertej/tools/pi0_gen_tools/run/lund_processors/ --track debug -n 2 -r --q2min 5 --out aao_norad_highq2  

#To submit all jobs in a directory to batch farm:
#./run/submit_jsubs.exe --jobsdir sub_warehouse/  
