#!/bin/bash


SCRIPTDIR="/projects/perinatal/peridata/paul/tractography/connectivity"
WORKDIR="/projects/perinatal/peridata/paul/EPRIME"


idListFile="ids.txt"

# Ignore lines in the file that start with a # character.
commentPattern=' *\#'

while read id
do
    if [[ "${id}" =~ ${commentPattern}  ]] ; then continue ; fi

    timeStamp=`date +'%Y%m%d-%H%M%S'`
    outputFile=${SCRIPTDIR}/output/output-ipsi-contra-${timeStamp}-${id}.txt
    command="run_get_ipsi_contra.sh ${id} &>  ${outputFile}"
    echo ${command}
    eval ${command}

    echo
    echo "#######################################################################"
    echo

done < ${idListFile}

