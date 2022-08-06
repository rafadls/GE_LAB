import string
import numpy as np
import sge
import pandas as pd
import os
import json
import itertools
import shutil
import subprocess
import sys
import argparse

from sge.parameters import params

from sge.engine import setup

def createFolder(folder):
    try:
        shutil.rmtree(mainPath + '/' + folder)
    except:
        pass
    try:
        os.makedirs(mainPath + '/' + folder)
    except:
        pass

# Se obtiene el path relativo
mainPath = os.path.abspath("")

#createFolder('results/')

for i in range(10):
    subprocess.check_call(['python','-m', 'problems.GRID.n', '--experiment_name','results/GE','--run', str(i), '--parameters', 'parameters/GRID/n.yml', '--algorithm', 'GE'])
    subprocess.check_call(['python','-m', 'problems.GRID.n', '--experiment_name','results/SGE','--run', str(i), '--parameters', 'parameters/GRID/n.yml', '--algorithm', 'SGE'])
    subprocess.check_call(['python','-m', 'problems.GRID.n', '--experiment_name','results/PGE','--run', str(i), '--parameters', 'parameters/GRID/n.yml', '--algorithm', 'PGE'])