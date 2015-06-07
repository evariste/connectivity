import sys
import argparse


import numpy as np
import graph_tool.all as gt


from connectivtyUtilsPA import readRawData
from connectivtyUtilsPA import matrixToGraph

from matplotlib import pyplot as plt

def main(*args):
  
  helpText = '''
Read a raw data matrix

find the mst of the graph at a range of thresholds starting at zero

mst seems to be the same for different thresholds, do not consider thresholds that 

lead to multiple components.
'''
  
  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)
  
  helpText = 'raw matrix file'
  parser.add_argument("filename", type=str, help=helpText)


  args = parser.parse_args()

  filename = args.filename

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
  
  # vertex indices for the edges
  # source indices and target indices
  e_s = np.zeros(nEdges, dtype=np.int)
  e_t = np.zeros(nEdges, dtype=np.int)

  i = 0
  for e in G.edges():
    e_s[i] = int(e.source())
    e_t[i] = int(e.target())
    i = i + 1
  
  w = G.edge_properties['weight'].a
  wMax = np.max(w) 
  w2 = (0.1 * wMax) + (wMax - w)
  w2prop = G.new_edge_property('double')
  w2prop.a = w2
  
  mstAll = np.zeros(data.shape)
  
  filt = G.new_edge_property('bool')
  
  wHi = np.percentile(data[data>0], 99)
  ts = np.linspace(0, wHi, 20)
  
  for t in ts:
    temp = data > t
    filt.a = temp[e_s, e_t]
    G.set_edge_filter(filt)
    
    _, compHist = gt.label_components(G)
    print len(compHist), t
    if len(compHist) > 1:
      break
    
    mst = gt.min_spanning_tree(G, weights=w2prop)
    G.set_edge_filter(None)
  
    for e in G.edges():
      if mst[e]:
        mstAll[e.source(), e.target()] += 1
      

  plt.imshow(mstAll,interpolation='nearest')
  temp = mstAll[mstAll > 0]
  print np.mean(temp), np.std(temp)
  plt.colorbar()
  plt.show()
  
  



if __name__ == '__main__':
  sys.exit(main(*sys.argv))


