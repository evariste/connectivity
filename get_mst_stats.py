import sys, argparse


import numpy as np

rootDir = '/projects/perinatal/peridata'
workDir = rootDir + '/paul/EPRIME'

tractSubDir = '001_diffusion_data/tractography/tracts'


def main(*args):
  
  helpText = '''
Sum the minimum spanning tree derived matrices for the e-prime group.
The MST matrices are derived from tractographies.
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

  helpText = 'input name of individual MST files (numpy array)'
  parser.add_argument('input', type=str, help=helpText)

  

  args = parser.parse_args()

  region_def = args.region_def
  measure = args.measure
  idFile = args.id_list
  outputFile = args.output
  mstFilename = args.input

  f = open(idFile)

  ids = map(lambda s: s[:-1], f.readlines())

  mstPath = (tractSubDir +
             '/' + region_def +
             '/' + measure + '/' +
             mstFilename)

  # Get size from first in list.
  dataFile = (workDir + '/' + ids[0] + '/' + mstPath)

  temp = np.load(dataFile)
  sumArr = np.zeros(temp.shape)

  for id in ids:
    print id

    dataFile = (workDir + '/' + id + '/' + mstPath)
    mstArr = np.load(dataFile)
    sumArr = sumArr + mstArr


  f.close()

  np.save(outputFile, sumArr)


if __name__ == '__main__':
  sys.exit(main(*sys.argv))





