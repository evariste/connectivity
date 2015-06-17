#/bin/bash

SCRIPTDIR='/home/paulaljabar/connectivity'

CIRCOS='/home/paulaljabar/packages/circos-0.67-7/bin/circos'

circosWorkDir='/home/paulaljabar/circos-scratch/mst-data-e-prime'

labelLookup=$SCRIPTDIR/aal-circos-lookup.csv


## USAGE:
min_num_args=2
if [ ! $# -ge $min_num_args ]; then
  echo "  Usage $0 [input] [outputBasename] <-threshold value>

  Generate circos plots (svg and png) for given input connectivity file.
  Given input.npy, provide outputBasename.{png,svg}, images for the 
  connectogram. 

Assumes the regions for the AAL regions 1 to 90.

Default threshold for selecting links is 0 unless specified.

"
  exit
fi

input=$1
shift

outname=$1
shift


threshold=0

while [[ ! $# = 0 ]]; do
    case $1 in
	-threshold)
	    shift
	    threshold=$1
	    shift
	    ;;
	*)
	    echo "Unrecognised argument : $1"
	    exit 65
	    ;;
    esac
done

echo "Input: $input"
echo "Output: $outname"
echo "Setting threshold to $threshold"


linkFile=${input/.npy/-links.txt}

# Threshold - Need to fix so that only edges with a probability of MST
# selection greater than, say, 25% are retained

cmd="python $SCRIPTDIR/conn_mat_to_circos_links.py \
 $input $labelLookup $linkFile -threshold $threshold"

echo $cmd
eval $cmd 

cmd="cp $linkFile $circosWorkDir/"
echo $cmd
eval $cmd

prevDir=`pwd`

cmd="cd $circosWorkDir"
echo $cmd
eval $cmd


mkdir -p ./data

cmd="./parsemap -map aal-map.txt -links maps.links.txt  -datadir ./data"
echo $cmd
eval $cmd


cmd="$CIRCOS  -conf etc/brain.conf"
echo $cmd
eval $cmd

cd $prevDir

cmd="cp $circosWorkDir/circos.svg ${outname}.svg"
echo $cmd
eval $cmd

cmd="cp $circosWorkDir/circos.png ${outname}.png"
echo $cmd
eval $cmd

