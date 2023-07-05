#!/bin/bash

# this script prints the line corresponding to the mag field configuratioon for OSG CLAS12 jobs

# Function to print the help message
function print_help {
    echo "Usage: get_config.sh -u [user_name] -n [job_number]"
    echo " "
    echo "Options:"
    echo "-h, --help                  Show brief help"
    echo "-u, --user_name             Specify user name"
    echo "-n, --job_number            Specify job number"
    exit 0
}

# Parse command line arguments
while (( "$#" )); do
  case "$1" in
    -u|--user_name)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        user_name=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    -n|--job_number)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        job_number=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    -h|--help)
      print_help
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

# Check if all required parameters were supplied
if [ -z "$user_name" ] || [ -z "$job_number" ]; then
    echo "Error: Both user name and job number must be supplied."
    print_help
    exit 1
fi

path='/lustre19/expphy/volatile/clas12/osg2/'$user_name'/job_'$job_number'/nodeScript.sh'

# Print the relevant line (line 125 as of 2023)
config=$(sed -n '125p' $path)
echo "$config"

