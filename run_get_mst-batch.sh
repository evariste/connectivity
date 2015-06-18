#!/bin/bash


source /projects/perinatal/peridata/paul/packages/python/envPA/bin/activate

export PYTHONPATH=/projects/perinatal/peridata/paul/scripts/python_scripts:${PYTHONPATH}

# set -vx

SCRIPTDIR="/projects/perinatal/peridata/paul/tractography/connectivity"
WORKDIR="/projects/perinatal/peridata/paul/EPRIME"


idListFile="ids.txt"

# Ignore lines in the file that start with a # character.
commentPattern=' *\#'

# For original connectivity matrices.
SCRIPTA='run_get_mst-conn-raw.sh'
# For ipsilateral-contralateral representations.
SCRIPTB='run_get_mst-ipsi_contra.sh'

# Choice!
SCRIPT=$SCRIPTB

while read id
do
    if [[ "${id}" =~ ${commentPattern}  ]] ; then continue ; fi

    timeStamp=`date +'%Y%m%d-%H%M%S'`
    outputFile=${SCRIPTDIR}/output/output-mst-${timeStamp}-${id}.txt
    command="${SCRIPT} ${id} &>  ${outputFile}"
    echo ${command}
    eval ${command}

    echo
    echo "#######################################################################"
    echo

done < ${idListFile}

