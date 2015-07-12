import sys
import argparse

import numpy as np

from connectivtyUtilsPA import readRawData

ops = {'add': np.add,
       'sub': np.subtract,
       'mul': np.multiply,
       'div': np.divide}

def main(*args):
  
  helpText = '''
  Apply a binary operaton elementwise to a pair of connectivity matrices 

    matrixA op matrixB matrixOut 

  Where the matrix files can be raw connectivty or numpy files.
'''
  
  parser = argparse.ArgumentParser(description=helpText,formatter_class=argparse.RawTextHelpFormatter)
  

  helpText = 'Connectivity matrix file A'
  parser.add_argument("filenameA", type=str, help=helpText)

  helpText = 'Operation: i.e. add/sub/mul/div'
  parser.add_argument("opName", type=str, help=helpText)

  helpText = 'Connectivity matrix file B'
  parser.add_argument("filenameB", type=str, help=helpText)

  helpText = 'Output numpy array for result'
  parser.add_argument('output', type=str, help=helpText)

  args = parser.parse_args()

  filenameA = args.filenameA
  opName = args.opName
  filenameB = args.filenameB
  outputName = args.output

  if filenameA[-4:] == '.raw':
    # Raw format
    dataA = readRawData(filenameA)
  elif filenameA[-4:] == '.npy':
    # Numpy array
    dataA = np.load(filenameA)

  if filenameB[-4:] == '.raw':
    # Raw format
    dataB = readRawData(filenameB)
  elif filenameB[-4:] == '.npy':
    # Numpy array
    dataB = np.load(filenameB)


  op = ops[opName]
  
  dataOut = op(dataA, dataB)

  np.save(outputName, dataOut)


if __name__ == '__main__':
  sys.exit(main(*sys.argv))


