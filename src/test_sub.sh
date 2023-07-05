#!/bin/sh

#creates 1 file with no submission that can be used for testing

python3.6 run_sims.py --base_dir /volatile/clas12/robertej --generator_type rad -n 1  --ebeam 10.604 --epmin 0.2 --epmax 10.604 --f18_in --w2min 3.5721 --q2min 0.9
