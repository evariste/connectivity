import sys
import argparse


import numpy as np
import graph_tool.all as gt


from connectivtyUtilsPA import readRawData
from connectivtyUtilsPA import matrixToGraph

from matplotlib import pyplot as plt

def main(*args):
  
  helpText = '''
Read a given raw matrix file from a tractography and find the minimum
spanning tree (MST). Save the MST to a numpy array with
the given output name.
'''
  
  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)
  
  helpText = 'raw matrix file'
  parser.add_argument("filename", type=str, help=helpText)

  helpText = 'Output numpy array for MST'
  parser.add_argument('output', type=str, help=helpText)
  
  args = parser.parse_args()

  filename = args.filename
  outputName = args.output
  
  data = readRawData(filename)

  G = matrixToGraph(data)

  # Expect 90 nodes, 8 of which are subcortical so that they are 
  # disconnected. This leaves 82 for the largest component
  lcomp = gt.label_largest_component(G)

  # Filter the graph so we only consider the 82 cortical nodes.
  G.set_vertex_filter(lcomp)

  nVertices = G.num_vertices()
  nEdges = G.num_edges()

  print nVertices, nEdges
  
  propW = G.edge_properties['weight']
  w = propW.a
  wMax = np.max(w) 
  w2 = (0.1 * wMax) + (wMax - w)
  w2prop = G.new_edge_property('double')
  w2prop.a = w2
  
    
  mst = gt.min_spanning_tree(G, weights=w2prop)
  
  treeW = 0.0
  
  temp = 0.0
  
  mstMat = np.zeros(data.shape)

  for e in G.edges():
    if mst[e]:
      s,t = e.source(), e.target()
      treeW += propW[e]
      mstMat[s,t] = 1
      
      temp += data[s,t]

      
  print treeW
  print temp
  
  temp = data[data > 0]
  for _ in range(10):
    ix = np.random.randint(0, nEdges, size=nVertices-1)
    print np.sum(temp[ix])
  
  

  
  np.save(outputName, mstMat)


  temp = np.load(outputName)
  plt.imshow(temp,interpolation='nearest')
  plt.show()


if __name__ == '__main__':
  sys.exit(main(*sys.argv))


