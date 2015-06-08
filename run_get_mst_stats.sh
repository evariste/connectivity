#!/bin/bash



# Script to perform modified probtrackx tractography


envScript='/Users/paulaljabar/work/scripts/python/pythonEnvs/surfaceAnalysis/bin/activate'
# envScript='/projects/perinatal/peridata/paul/packages/python/envPA/bin/activate'

source $envScript


pyUtilDir='/projects/perinatal/peridata/paul/scripts/python_scripts'
export PYTHONPATH=${pyUtilDir}:${PYTHONPATH}


idFile='ids.txt'

labelNames="randomLabels-250  randomLabels-282 unc-aal unc-aal-with-subcort"

measures="anisotropy probability"

for labelSet in $labelNames
do

    for measure in $measures
    do
	output="output/mst-stats-$labelSet-$measure"

	command="python get_mst_stats.py $labelSet $measure $idFile $output"

	echo ${command}
	eval ${command}
	echo
    done

done





