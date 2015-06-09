import sys
import argparse

import numpy as np
from graph_tool.topology import label_largest_component, min_spanning_tree

from connectivtyUtilsPA import readRawData, matrixToGraph

def main(*args):
  
  helpText = '''
Read a given raw connectivity matrix file from a tractography and find the minimum
spanning tree (MST). Save the MST to a numpy array with
the given output name.  Repeat the process a number of times on
versions of the original connectivity matrix with noise added.

Accumulate the scores for each edge, i.e. the number of times it
is in the MST over all repetitions. Default number of repetitions = 100.

Default noise value added drawn uniformly from zero to 5th percentile of
distribution of differences between edge-weights.

Intended for use with UNC AAL based regions in the tractography.
'''
  
  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)
  
  helpText = 'raw matrix file'
  parser.add_argument("filename", type=str, help=helpText)

  helpText = 'Output numpy array for MST'
  parser.add_argument('output', type=str, help=helpText)

  helpText = 'Repetitions on adding noise'
  parser.add_argument('-reps', type=int, help=helpText, default=100)

  helpText = 'noise level: (default) -1 -> estimate from data, 0 or higher, use given value'
  parser.add_argument('-noise', type=float, help=helpText, default=-1)

  args = parser.parse_args()

  filename = args.filename
  outputName = args.output
  nReps = args.reps
  width = args.noise
  
  data = readRawData(filename)

  G = matrixToGraph(data)

  # Expect 90 nodes, 8 of which are subcortical so that they are 
  # disconnected. This leaves 82 for the largest component
  lcomp = label_largest_component(G)

  # Filter the graph so we only consider the 82 cortical nodes.
  G.set_vertex_filter(lcomp)

  nVertices = G.num_vertices()
  nEdges = G.num_edges()

  print '(nodes, edges) in largest component : (' , nVertices, ', ', nEdges , ')'

  if width < 0:
    temp = np.tri(data.shape[0])
    temp = temp * data
    temp = temp[temp > 0]

    nVals = temp.size
    diffs = np.zeros(nVals * (nVals-1) / 2)
    n = 0
    for i in range(nVals-1):
      for j in range(i+1, nVals):
        diffs[n] = np.fabs( temp[i] - temp[j] )
        n += 1

    width = np.percentile(diffs, 5)

  print 'adding noise with width ', width
  print 'repeating ', nReps, ' times'
  
  propW = G.edge_properties['weight']
  w = propW.a
  wMax = np.max(w) 
  w2 = (0.1 * wMax) + (wMax - w)
  w2prop = G.new_edge_property('double')
  w2prop.a = w2
  w2propNoise = G.new_edge_property('double')

  mstMat = np.zeros(data.shape)
  
  for i in range(nReps):
    noiseVals = 2.0 * width * (np.random.rand(nEdges) - 0.5 )
    w2propNoise.a = w2 + noiseVals
    mst = min_spanning_tree(G, weights=w2propNoise)
  
    treeW = 0.0
  

    for e in G.edges():
      if mst[e]:
        s,t = e.source(), e.target()
        treeW += propW[e]
        mstMat[s,t] += 1

      
    print 'Total weight for MST = ',
    print '{:0.3f}'.format(treeW)
  
  np.save(outputName, mstMat)




if __name__ == '__main__':
  sys.exit(main(*sys.argv))


