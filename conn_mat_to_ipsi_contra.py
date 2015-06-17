import sys
import argparse

import numpy as np
from connectivtyUtilsPA import readRawData

def main(*args):

  helpText = '''
Take a connectivty matrix based on the 90 region set from the 
AAL atlas and provide a new representation where data from all 
pairs of ipsilateral and all pairs of contralateral edges are 
combined.

All regions in the input matrix appear in left (L) and right (R) versions.

All regions in the output matrix appear in ipsilateral (I) and 
contralateral (C) versions.

I.e. for region A and region B, with left and right version A.L, A.R,
B.L, B.R, the weights of the edges (A.L,B.L), (A.R,B.R), (B.L,A.L),
(B.R,A.R) are combined (added) to make a single ipsilateral edge
between the nodes A.I and B.I.

Also, the weights of edges (A.L,B.R), (A.R,B.L), (B.R,A.L), 
(B.L,A.R) are combined into a weight for a single contralateral edge (A.C,
B.C). 

See comments in script for detail of region ordering.

'''


  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)

  helpText = 'Connectivity matrix file, .raw or .npy format'
  parser.add_argument("filename", type=str, help=helpText)

  helpText = 'Output numpy array for ipsi-contra version'
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
  # Order in input array is

  # Region index   0  0  1  1  2  2 ... 43 43 44 44
  # Array  Index   0  1  2  3  4  5 ... 86 87 88 89
  #                L  R  L  R  L  R ... L  R  L  R

  # Output data has ipsilateral, contralateral instead of L/R
  # Region index   0  0  1  1  2  2 ... 43 43 44 44
  # Array  Index   0  1  2  3  4  5 ... 86 87 88 89
  #                I  C  I  C  I  C ... I  C  I  C

  w2 = np.zeros(w.shape)

  for i in range(44):
    a_L = 2 * i
    a_R = 2 * i + 1
    a_I = a_L
    a_C = a_R

    for j in range(i+1, 45):
      b_L = 2 * j
      b_R = 2 * j + 1
      b_I = b_L
      b_C = b_R

      w2[a_I, b_I] = (w[a_L, b_L] +
                      w[a_R, b_R] +
                      w[b_L, a_L] +
                      w[b_R, a_R])
      w2[a_C, b_C] = (w[a_L, b_R] +
                      w[a_R, b_L] +
                      w[b_R, a_L] +
                      w[b_L, a_R])

  # Symmetrize
  w2 = np.maximum(w2, w2.T)

  np.save(outputName, w2)


if __name__ == '__main__':
  sys.exit(main(*sys.argv))


