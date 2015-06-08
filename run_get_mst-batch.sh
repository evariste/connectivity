#!/bin/bash


source /projects/perinatal/peridata/paul/packages/python/envPA/bin/activate

export PYTHONPATH=/projects/perinatal/peridata/paul/scripts/python_scripts:${PYTHONPATH}

# set -vx

SCRIPTDIR="/projects/perinatal/peridata/paul/tractography/connectivity"
WORKDIR="/projects/perinatal/peridata/paul/EPRIME"


idListFile="ids.txt"

# Ignore lines in the file that start with a # character.
commentPattern=' *\#'

while read id
do
    if [[ "${id}" =~ ${commentPattern}  ]] ; then continue ; fi

    timeStamp=`date +'%Y%m%d-%H%M%S'`
    outputFile=${SCRIPTDIR}/output/output-mst-${timeStamp}-${id}.txt
    command="run_get_mst.sh ${id} &>  ${outputFile}"
    echo ${command}
    eval ${command}

    echo
    echo "#######################################################################"
    echo

done < ${idListFile}

