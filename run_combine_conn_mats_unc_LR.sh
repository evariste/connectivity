#!/bin/bash


ROOTDIR='/projects/perinatal/peridata'
#ROOTDIR='/Users/paulaljabar/work/cdb/e-prime/from-peridata'

SCRIPTDIR="${ROOTDIR}/paul/tractography/connectivity"
DATADIR="${ROOTDIR}/EPRIME"
WORKDIR="${ROOTDIR}/paul/EPRIME"

tractPath='001_diffusion_data/tractography/tracts'

#envScript='/Users/paulaljabar/work/scripts/python/pythonEnvs/surfaceAnalysis/bin/activate'
envScript='${ROOTDIR}/paul/packages/python/envPA/bin/activate'

source $envScript


#pyUtilDir='/Users/paulaljabar/work/scripts/python'
pyUtilDir='${ROOTDIR}/paul/scripts/python_scripts'
export PYTHONPATH=${pyUtilDir}:${PYTHONPATH}


idFile='ids.txt'

measures="anisotropy probability"


labelNames="unc-aal unc-aal-with-subcort"


ids=`cat $idFile`

for labelSet in $labelNames
do

    for ID in $ids
    do

	for measure in $measures
	do
	    fileA=`ls ${WORKDIR}/${ID}/${tractPath}/$labelSet/$measure/$measure*raw`	
	    fileB=`ls ${WORKDIR}/${ID}/${tractPath}/$labelSet-reflect/$measure/$measure*raw`

	    fileOut="${WORKDIR}/${ID}/${tractPath}/$labelSet-both/$measure/$measure.npy"
	    mkdir -p `dirname $fileOut`


	    command="python conn_mat_maths.py $fileA add $fileB $fileOut"
	    echo ${command}
	    eval ${command}
	    echo
	done
    done

done


#########################################################
