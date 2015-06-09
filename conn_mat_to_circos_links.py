import sys, argparse


import numpy as np

rootDir = '/projects/perinatal/peridata'
workDir = rootDir + '/paul/EPRIME'

tractSubDir = '001_diffusion_data/tractography/tracts'


def main(*args):
  
  helpText = '''
  Read a connectivity matrix in numpy format based on a region definition (e.g. AAL labels)
  
  Read a look up table to convert region indices into left/right + short circos names.
  
  Produce a links file for circos to create a connectogram.
'''
  
  parser = argparse.ArgumentParser(description=helpText) 
  # ,formatter_class=argparse.RawTextHelpFormatter)

  helpText = 'Connectivity matrix (*.npy)'
  parser.add_argument("connMat", type=str, help=helpText)
  
  helpText = 'Region lookup file (*.csv)'
  parser.add_argument("regionLUT", type=str, help=helpText)

  helpText = 'Output links text file.'
  parser.add_argument("output", type=str, help=helpText)

  helpText = 'Threshold: Default 0'
  parser.add_argument('-threshold', type=float, help=helpText, default=0.0)
  args = parser.parse_args()

  connMatFile = args.connMat
  lutFile = args.regionLUT
  outputFile = args.output
  threshold = args.threshold
  
  print 'Threshold at ', threshold
  
  

  f = open(lutFile)  
  lines = map(lambda s: s[:-1], f.readlines())
  f.close()

  # skip header
  lines = lines[1:]
  
  side = {}
  shortName = {}
  
  for line in lines:
    fields = line.split(',')
    labelNumber = int(fields[0])
    labelIndex = labelNumber - 1
    side[labelIndex] = fields[3]
    shortName[labelIndex] = fields[5]
    
   
    
  
  mat = np.load(connMatFile)

  nNodes = mat.shape[0]
  
  if (len(mat.shape) > 2) or (mat.shape[1] <> nNodes):
    raise Exception('Expecting a 2D square array')
  
  fOut = open(outputFile, 'w')
  # Links file has format
  
  # hemisphere parcelation hemisphere parcelation connection_type connection_score
  # Eg.     r FSup l Hip 1 0.5
  fmtOut = '{:s} {:s} {:s} {:s} 1 {:0.2f}\n'
  
  maxVal = np.max(mat)
  
  
  for i in range(nNodes-1):
    srcName = shortName[i]
    srcSide = side[i]
    for j in range(i+1, nNodes):
      val = mat[i,j]
      if val > threshold:
        tgtName = shortName[j]
        tgtSide = side[j]
        strOut = fmtOut.format(srcSide, srcName, tgtSide, tgtName, val/maxVal)
        fOut.write( strOut )
    

  fOut.close()


if __name__ == '__main__':
  sys.exit(main(*sys.argv))





