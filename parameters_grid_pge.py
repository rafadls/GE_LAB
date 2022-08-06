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

df_grid = pd.read_csv(os.sep.join([mainPath, "grid_parameters.csv"]))

createFolder('results/')

for index, row in df_grid.iterrows():
    problem = str(row['problem'])
    parameters = str(row['parameters'])
    runs = row['runs']
    generations = row['generations']
    popsize = row['popsize']
    learning_factor = row['learning_factor']
    adaptive_increment_p = row['adaptive_increment_p']
    adaptive_increment = adaptive_increment_p*learning_factor
    elitism_p = row['elitism_p']
    elitism = int((elitism_p*popsize)//1)
    prob_crossover = row['prob_crossover']
    prob_mutation = row['prob_mutation']
    algorithm = 'PGE'
    for i in range(runs):
        subprocess.check_call(['python','-m', 'problems.GRID.' + problem,'--learning_factor',str(learning_factor),'--adaptive_increment',str(adaptive_increment), '--experiment_name','results/'+ problem + '/' + str(index), '--parameters', 'parameters/GRID/' + parameters, '--algorithm', algorithm, '--run', str(i),'--generations',str(generations),'--popsize',str(popsize),'--elitism',str(elitism),'--prob_crossover',str(prob_crossover),'--prob_mutation',str(prob_mutation)])

#subprocess.check_call(['python','graph.py'])