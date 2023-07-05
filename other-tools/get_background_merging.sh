\#!/bin/bash

#this script prints the line corresponding to the mag field configuratioon for OSG CLAS12 jobs

read -p "Enter user name number (e.g. robertej): " user_name

read -p "Enter job number (e.g. 5702): " job_number

path='/lustre19/expphy/volatile/clas12/osg2/'$user_name'/job_'$job_number'/nodeScript.sh'


# Print the relevant line (line 66 as of 2023)
config=$(sed -n '66p' $path)
echo "$config"
