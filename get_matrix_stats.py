import numpy as np

import sys
import argparse


from connectivtyUtilsPA import readRawData



def main(*args):
  
  helpText = "\
Generate statistics for a matrix output from tractography.\n \
Output:\n \
Number of elements\n\
Number of non-zero elements \n \n \
Then, for all elements: \n \
  Min value \n \
  Median\n \
  Mean\n \
  Max\n \
Then, for non-zero elements \n \
  Min value\n \
  Median\n \
  Mean\n \
  Max\n \
"
  
  parser = argparse.ArgumentParser(description=helpText, formatter_class=argparse.RawTextHelpFormatter)
  
  helpText = 'raw matrix file'
  parser.add_argument("filename", type=str, help=helpText)

  helpText = 'Precision of main output stats, default = 3'
  parser.add_argument('-precision', type=int, help=helpText, default=3)

  args = parser.parse_args()

  filename = args.filename
  precision = args.precision

  data = readRawData(filename)


  ix = data > 0
  temp = np.ravel(data[ix])
  output = (np.min(temp), np.median(temp), np.mean(temp), np.max(temp))

  
  print '{:d} {:d}'.format( data.shape[0], len(temp) ),

  outStr='{:0.' + str(precision) + 'f}'

  for val in output:
    print outStr.format(val),
  print



if __name__ == '__main__':
  sys.exit(main(*sys.argv))


