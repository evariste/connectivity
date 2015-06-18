#!/bin/bash

## USAGE:
min_num_args=1
if [ ! $# -ge $min_num_args ]; then
  echo "  Usage $0 [ID]

   Get Minimum spanning trees for ipsi-contra representations of connectivty.
   Assumes a 90 region AAL labeling was used for tractography.
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


labelNames="unc-aal unc-aal-with-subcort"

# Take two components from the ipsi-contra matrices as the two types
# of edges are in distinct sub-graphs. The minimum spanning tree will
# then be obtained for each sub-graph



for labelSet in $labelNames 
do 
    currDir=${tractDir}/${labelSet}

    # Get MST in I-C representation.
    dataFile=${currDir}/anisotropy/ipsi-con.npy
    mstFile=${currDir}/anisotropy/mst-ipsi-con.npy

    command="python conn_mat_to_mst.py ${dataFile} ${mstFile} -comps 2"
    echo ${command}
    eval ${command}
    echo

    # Recover MST in ordinary connectivity representation
    mstFileRecovered=${mstFile/.npy/-recover.npy}
    command="python ipsi_contra_to_conn_mat.py ${mstFile} ${mstFileRecovered}"
    echo ${command}
    eval ${command}
    echo

    # Get MST in I-C representation.
    dataFile=${currDir}/probability/ipsi-con.npy
    mstFile=${currDir}/probability/mst-ipsi-con.npy

    command="python conn_mat_to_mst.py ${dataFile} ${mstFile} -comps 2"
    echo ${command}
    eval ${command}
    echo

    # Recover MST in ordinary connectivity representation
    mstFileRecovered=${mstFile/.npy/-recover.npy}
    command="python ipsi_contra_to_conn_mat.py ${mstFile} ${mstFileRecovered}"
    echo ${command}
    eval ${command}
    echo


done





