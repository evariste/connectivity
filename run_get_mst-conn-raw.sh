#!/bin/bash

## USAGE:
min_num_args=1
if [ ! $# -ge $min_num_args ]; then
  echo "  Usage $0 [ID]

   Get Minimum spanning trees for tractography results for a scan.

"
  exit
fi


source /projects/perinatal/peridata/paul/packages/python/envPA/bin/activate

export PYTHONPATH=/projects/perinatal/peridata/paul/scripts/python_scripts:${PYTHONPATH}

SCRIPTDIR="/projects/perinatal/peridata/paul/tractography/connectivity"
DATADIR="/projects/perinatal/peridata/EPRIME"
WORKDIR="/projects/perinatal/peridata/paul/EPRIME"


id=$1


# Where are the tractography results?
tractDir=${WORKDIR}/${id}/001_diffusion_data/tractography/tracts


labelNames="randomLabels-250  randomLabels-282 unc-aal unc-aal-with-subcort"
labelNames="unc-aal-both unc-aal-with-subcort-both"


for labelSet in $labelNames
do
    currDir=${tractDir}/${labelSet}

    dataFile=${currDir}/anisotropy/*.raw
    # For combined unc and reflected data, the output is in numpy format
    dataFile=${currDir}/anisotropy/anisotropy.npy

    mstFile=${currDir}/anisotropy/mst.npy

    command="python conn_mat_to_mst.py ${dataFile} ${mstFile} "
    echo ${command}
    eval ${command}
    echo

    # probability data gives non-informative connectivity
    # dataFile=${currDir}/probability/*.raw
    # mstFile=${currDir}/probability/mst.npy

    # command="python conn_mat_to_mst.py ${dataFile} ${mstFile} "
    # echo ${command}
    # eval ${command}
    # echo

done





