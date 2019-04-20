#! /usr/bin/env python

'''

python stats.py ../path/result.json


comments
========
Wrapper to use original OASC result evaluation

Author: HearNest

'''

import os
import csv
import sys
from subprocess import Popen
import subprocess

def main(args):
  if len(args) == 0:
    sys.exit('Missing Arg, E.g. python cv_stats.py [file path to jsons, e.g. ../results-aslib/autok/MAXSAT12-PMS]')

  jsonpath = args[0]
  if jsonpath[-1] != '/':
    jsonpath +='/' 

  if not os.path.exists(jsonpath):
    print 'File not found',jsonpath
    sys.exit()

  myhost = os.uname()[1]
  

  scenario = jsonpath.split("/")[-2]
  approach = jsonpath.split("/")[-3]
  # scenario =  filename.split(".")[0]


  root_arr = os.path.realpath(__file__).split('/')[:-1]
  root = '/'.join(root_arr) 
  script = root+'/validation/validate_cli.py'

  outdir = root+'/tmp'
  if not os.path.exists(outdir):
    os.makedirs(outdir)

  outputfile = root+'/tmp/'+myhost+'.txt'
  with open(outputfile, 'w+') as outfile:
    outfile.write("")
  f = open(outputfile, "a")
  for fold in xrange(1,11):
    result_file = jsonpath +'/test_1_'+str(fold)+".json"
    print 'running for ',result_file
    if not os.path.exists(result_file):
      print 'File not found',result_file
      sys.exit()

    test_folder = root+'/data/aslib-v2.0/'+scenario+'/cv_'+scenario+'/test_1_'+str(fold)
    train_folder = root+'/data/aslib-v2.0/'+scenario+'/cv_'+scenario+'/train_1_'+str(fold)

    # test_folder = root+'/data/aslib-/'+scenario+'/cv_'+scenario+'/test_1_'+str(fold)
    # train_folder = root+'/data/aslib-icon/'+scenario+'/cv_'+scenario+'/train_1_'+str(fold)

    cmd = 'python3 ' + script + ' --result_fn '  + result_file +' --test_as ' + test_folder + ' --train_as  ' + train_folder 
    print cmd
    subprocess.call(cmd.split(), stdout=f)

  # print 'ok',scenario,jsonpath,approach

  scores = []
  with open(outputfile) as ff:
    token = "Gap closed:"
    for line in ff:
      if token in line:
        scores.append(float(line.split(token)[1].strip()))

  print '==================='
  print scores
  if len(scores) != 10:
    sys.exit('There are not enough results of ten-fold')
  else:  
    print scenario, round(sum(scores)/10,2)


if __name__ == '__main__':
  main(sys.argv[1:])
  