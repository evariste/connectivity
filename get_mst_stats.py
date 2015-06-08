import sys, argparse


import numpy as np

rootDir = '/Users/paulaljabar/work/cdb/e-prime/from-peridata'
workDir = rootDir + '/paul/EPRIME'

tractSubDir = '001_diffusion_data/tractography/tracts'

temp = 'EP1009/001_diffusion_data/tractography/tracts/unc-aal/anisotropy/mst.npy'

def main(*args):
  
  helpText = '''
Find the number of times an edge appears in the minimum
spanning trees of a set of tractographies for the e-prime
group.

Need to specify which region definition is being used:

randomLabels-250  randomLabels-282 unc-aal unc-aal-with-subcort


'''
  
  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)

  helpText = 'region definition: one of (randomLabels-250  randomLabels-282 unc-aal unc-aal-with-subcort)'
  parser.add_argument("region_def", type=str, help=helpText)
  
  helpText = 'measure: one of (anisotropy probability)'
  parser.add_argument("measure", type=str, help=helpText)

  helpText = 'List of scan IDs'
  parser.add_argument("id_list", type=str, help=helpText)

  helpText = 'Output numpy array for MST summary data'
  parser.add_argument('output', type=str, help=helpText)
  
  args = parser.parse_args()

  region_def = args.region_def
  measure = args.measure
  idFile = args.id_list
  outputFile = args.output

  f = open(idFile)

  ids = map(lambda s: s[:-1], f.readlines())

  # Get size from first in list.
  dataFile = (workDir + '/' + ids[0] + '/' + tractSubDir +
               '/' + region_def +
               '/' + measure + '/mst.npy')

  temp = np.load(dataFile)
  sumArr = np.zeros(temp.shape)


  for id in ids:
    print id

    dataFile = (workDir + '/' + id + '/' + tractSubDir +
                 '/' + region_def +
                 '/anisotropy/mst.npy')

    print dataFile

    mstArr = np.load(dataFile)
    sumArr = sumArr + mstArr


  f.close()

  np.save(outputFile, sumArr)


if __name__ == '__main__':
  sys.exit(main(*sys.argv))





