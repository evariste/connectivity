import sys
import argparse

import numpy as np
from connectivtyUtilsPA import readRawData

def main(*args):
  
  helpText = '''
Convert 
'''
  
  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)
  
  helpText = 'Matrix file containing ipsilateral and contralateral data, .npy format'
  parser.add_argument("filename", type=str, help=helpText)

  helpText = 'Output numpy array for standard AAL connectivity version'
  parser.add_argument('output', type=str, help=helpText)

  args = parser.parse_args()

  filename = args.filename
  outputName = args.output

  #############################################


  if filename[-4:] == '.raw':
    # Raw format
    w = readRawData(filename)
  elif filename[-4:] == '.npy':
    # Numpy array
    w = np.load(filename)

  nRegions = 90
  r,c = w.shape
  if (r <> nRegions) or (c <> nRegions):
    raise Exception('convert_raw_mat_to_ipsi_contra : expecting 90 regions')

  # Each region has a L/R version
  # Order in input array is divided into ipsilateral, contralateral

  # Region index   0  0  1  1  2  2 ... 43 43 44 44
  # Array  Index   0  1  2  3  4  5 ... 86 87 88 89
  #                I  C  I  C  I  C ... I  C  I  C

  # Output data is arranged by L/R
  # Region index   0  0  1  1  2  2 ... 43 43 44 44
  # Array  Index   0  1  2  3  4  5 ... 86 87 88 89
  #                L  R  L  R  L  R ... L  R  L  R

  w2 = np.zeros(w.shape)

  for i in range(44):
    a_I = 2 * i
    a_C = 2 * i + 1
    a_L = a_I
    a_R = a_C
    for j in range(i+1, 45):
      b_I = 2 * j
      b_C = 2 * j + 1
      b_L = b_I
      b_R = b_C

      w2[a_L, b_R] = 0.25 * w[a_C, b_C] 
      w2[a_R, b_L] = 0.25 * w[a_C, b_C] 
      w2[a_L, b_L] = 0.25 * w[a_I, b_I]
      w2[a_R, b_R] = 0.25 * w[a_I, b_I]


  # Symmetrize
  w2 = np.maximum(w2, w2.T)


  np.save(outputName, w2)


if __name__ == '__main__':
  sys.exit(main(*sys.argv))


