#!/bin/bash



# Script to perform modified probtrackx tractography


# envScript='/Users/paulaljabar/work/scripts/python/pythonEnvs/surfaceAnalysis/bin/activate'
envScript='/projects/perinatal/peridata/paul/packages/python/envPA/bin/activate'

source $envScript


pyUtilDir='/projects/perinatal/peridata/paul/scripts/python_scripts'
export PYTHONPATH=${pyUtilDir}:${PYTHONPATH}


idFile='ids.txt'

measures="anisotropy probability"

run_for_conn_mats()
{
    labelNames="randomLabels-250  randomLabels-282 unc-aal unc-aal-with-subcort"

    for labelSet in $labelNames
    do

	for measure in $measures
	do
	    output="output/mst-stats-$labelSet-$measure"
	    command="python get_mst_stats.py $labelSet $measure $idFile $output mst.npy"
	    echo ${command}
	    eval ${command}
	    echo
	done

    done
}

#########################################################

run_for_ipsi_contra_mats()
{
    labelNames="unc-aal unc-aal-with-subcort"

    for labelSet in $labelNames
    do

	for measure in $measures
	do
	    output="output/mst-stats-ic-$labelSet-$measure"
	    command="python get_mst_stats.py \
$labelSet $measure $idFile \
$output mst-ipsi-con-recover.npy"
	    echo ${command}
	    eval ${command}
	    echo
	done

    done
}

#########################################################

#  run_for_conn_mats

run_for_ipsi_contra_mats





