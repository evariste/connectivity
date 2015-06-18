#!/bin/bash


## USAGE:
min_num_args=1
if [ ! $# -ge $min_num_args ]; then
  echo "  Usage $0 [ID]

   Convert connectivity from tractography results for a scan
   into an ipsilateral-contralateral representation. 

   Assumes a 90 region AAL atlas label set was used for the 
   tractography.
"
  exit
fi


source /projects/perinatal/peridata/paul/packages/python/envPA/bin/activate

export PYTHONPATH=/projects/perinatal/peridata/paul/scripts/python_scripts:${PYTHONPATH}

SCRIPTDIR="/projects/perinatal/peridata/paul/tractography/connectivity"
DATADIR="/projects/perinatal/peridata/EPRIME"
WORKDIR="/projects/perinatal/peridata/paul/EPRIME"

# SCRIPTDIR="/home/paulaljabar/connectivity"
# DATADIR="/mnt/hgfs/paulaljabar/work/cdb/e-prime/from-peridata/EPRIME/"
# WORKDIR="/mnt/hgfs/paulaljabar/work/cdb/e-prime/from-peridata/paul/EPRIME/"



id=$1


# Where are the tractography results?
tractDir=${WORKDIR}/${id}/001_diffusion_data/tractography/tracts


labelNames="unc-aal unc-aal-with-subcort"


for labelSet in $labelNames
do
    currDir=${tractDir}/${labelSet}

    dataFile=${currDir}/anisotropy/*.raw
    ipsiConFile=${currDir}/anisotropy/ipsi-con.npy

    command="python conn_mat_to_ipsi_contra.py ${dataFile} ${ipsiConFile} "
    echo ${command}
    eval ${command}
    echo

    dataFile=${currDir}/probability/*.raw
    ipsiConFile=${currDir}/probability/ipsi-con.npy

    command="python conn_mat_to_ipsi_contra.py ${dataFile} ${ipsiConFile} "
    echo ${command}
    eval ${command}
    echo

done





