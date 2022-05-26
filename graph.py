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
import matplotlib.pyplot as plt
from sge.parameters import params

from sge.engine import setup


formula_dict = {
    'Koza-1':r"$x^4 + x^3 + x^2 + x$", 
    'Koza-2': r"$x^5 - 2x^3 + x$", 
    'Koza-3': r"$x^6 - 2x^4 + x^2$", 
    'Nguyen-1': r"$x^3 + x^2 + x$", 
    'Nguyen-2': r"$x^4 + x^3 + x^2 + x$", 
    'Nguyen-3': r"$x^5 + x^4 + x^3 + x^2 + x$", 
    'Nguyen-4': r"$x^6 + x^5 + x^4 + x^3 + x^2 + x$", 
    'Nguyen-5': r"$sin(x^2)cos(x)-1$", 
    'Nguyen-6': r"$sin(x) + sin(x + x^2)$", 
    'Nguyen-7': r"$ln(x+1) + ln(x^2 + 1)$", 
    'Nguyen-8': r"$\sqrt{x}$", 
    'Nguyen-9': r"$sin(x) + sin(y^2)$",
    'Nguyen-10': r"$2sin(x)cos(y)$", 
    'Sin': r"$sin(x)$",
    'Rout': r"$R_{out}$",
    'Hcomb': r"$h_{comb}$", 
}

problems_array = os.listdir('results/')

for problem in problems_array:
    problem_path = 'results/' + problem + '/'
    algorithms_array = os.listdir(problem_path)
    df_fitness = pd.DataFrame()
    df_valid = pd.DataFrame()
    for algorithm in algorithms_array:
        algorith_path = problem_path + algorithm + '/'
        runs_array = os.listdir(algorith_path)
        fitness_list = []
        valid_list = []
        for run in runs_array:
            run_path = algorith_path + run + '/'
            df = pd.read_csv(run_path + 'progress_report.csv', names=['fitness', 'mean', 'std', 'valids'])
            fitness_list.append(df['fitness'])
            valid_list.append(df['valids'])
        fitness_array = np.asarray(fitness_list)
        valid_array = np.asarray(valid_list)
        df_fitness[algorithm] = fitness_array.mean(axis=0)
        df_valid[algorithm] = valid_array.mean(axis=0)
    fig, axis = plt.subplots(1,2, figsize=(18,10))
    fig.suptitle(problem + ': ' + formula_dict[problem] + ' , runs: ' + str(len(runs_array)) ,fontsize=25)
    df_fitness.plot(ax=axis[0])
    axis[0].set_title('Fitness',fontsize=15)
    axis[0].set_xlabel('Generations')
    axis[0].set_ylabel('Fitness')

    df_valid.plot(ax=axis[1])
    axis[1].set_title('Valid percentage of individuals',fontsize=15)
    axis[1].set_xlabel('Generations')
    axis[1].set_ylabel('Valid individuals')
    plt.savefig('results/' + problem + '.png')