import random
import sys
import numpy as np
import sge.grammar_sge as grammar_sge
import sge.grammar_pge as grammar_pge
import sge.grammar_ge as grammar_ge
import sge.logger as logger
from datetime import datetime
from tqdm import tqdm
from sge.operators.recombination import crossover
from sge.operators.mutation import mutate
from sge.operators.selection import tournament
from sge.parameters import (
    params,
    set_parameters,
    load_parameters
)
from random import randint, shuffle
from sge.mapper import mapper_GE, mapper_PGE
from sge.functions_pge import update_probs
import copy

import re
from scipy.optimize import minimize
from multiprocessing import Process, Queue
import time
from numpy import nan

import warnings

class TookTooLong(Warning):
    pass

class MinimizeStopper(object):
    def __init__(self, max_sec=20):
        self.max_sec = max_sec
        self.start = time.time()
    def __call__(self, xk=None):
        elapsed = time.time() - self.start
        if elapsed > self.max_sec:
            warnings.warn("Terminating optimization: time limit reached",
                          TookTooLong)
        else:
            # you might want to report other stuff here
            print("Elapsed: %.3f sec" % elapsed)


def generate_random_individual():
    genotype, tree_depth = None, None
    if params['ALGORITHM']=='SGE':
        genotype = [[] for key in grammar_sge.get_non_terminals()]
        tree_depth = grammar_sge.recursive_individual_creation(genotype, grammar_sge.start_rule()[0], 0)
    elif params['ALGORITHM']=='GE':
        genotype = [randint(0, params['CODON_SIZE']) for _ in range(params['SIZE_GENOTYPE'])]
    elif params['ALGORITHM']=='PGE':
        genotype = [np.random.uniform() for _ in range(params['SIZE_GENOTYPE'])]
    return {'genotype': genotype, 'fitness': None, 'tree_depth' : tree_depth}


def make_initial_population():
    for i in range(params['POPSIZE']):
        yield generate_random_individual()


def evaluate(ind, eval_func, OPTIMIZE=False):
    phen, tree_depth, other_info, quality = None, None, None, np.inf
    if ind['fitness'] is None:
        if params['ALGORITHM']=='SGE':
            mapping_values = [0 for i in ind['genotype']]
            ind['original_phenotype'], tree_depth = grammar_sge.mapping(ind['genotype'], mapping_values)
            ind['mapping_values'] = mapping_values
        elif params['ALGORITHM']=='GE':
            ind['original_phenotype'], genome, tree, nodes, invalid, tree_depth, used_codonsmapper = mapper_GE(ind['genotype'])
        elif params['ALGORITHM']=='PGE':
            ind['original_phenotype'], ind['gram_counter'] = mapper_PGE(ind['genotype'])
        phen = Get_phtnotype_time(ind['original_phenotype'],eval_func, OPTIMIZE)
        try:
            quality, other_info = eval_func.evaluate(phen)
        except:
            pass
        if quality == None:
            quality = np.inf
        ind['phenotype'] = phen
        ind['fitness'] = quality
        ind['other_info'] = other_info
        ind['tree_depth'] = tree_depth
    elif (not 'phenotype' in ind.keys()) or OPTIMIZE:        
        phen = Get_phtnotype_time(ind['original_phenotype'],eval_func, OPTIMIZE)
        try:
            quality, other_info = eval_func.evaluate(phen)
        except:
            pass
        if quality == None:
            quality = np.inf
        ind['phenotype'] = phen
        ind['fitness'] = quality
        ind['other_info'] = other_info


def Get_phtnotype_time(phenotype, fitness_function, OPTIMIZE):
    def f(phenotype, fitness_function, OPTIMIZE, queue):
        res = Get_phenotype(phenotype, fitness_function, OPTIMIZE)
        queue.put(res)

    q = Queue()
    p = Process(target=f, args=(phenotype, fitness_function, OPTIMIZE, q))
    max_time = 30
    t0 = time.time()

    p.start()
    while time.time() - t0 < max_time:
        p.join(timeout=1)
        if not p.is_alive():
            break

    if p.is_alive():
        #process didn't finish in time so we terminate it
        p.terminate()
        result = Get_phenotype(phenotype, fitness_function, False)
    else:
        result = q.get()
    return result


def Get_phenotype(phenotype, fitness_function, OPTIMIZE):
    minimize_stopper = MinimizeStopper()
    p = r"Constant"
    n_constants = len(re.findall(p, phenotype))

    replace_phenotype = phenotype
    for i in range(n_constants):
      replace_phenotype = replace_phenotype.replace('Constant', 'c[' + str(i) + ']',1)

    def eval_ind(c):
        aux = replace_phenotype
        for i in range(len(c)):
            aux = aux.replace('c[' + str(i) + ']', str(c[i]))
        return fitness_function.evaluate(aux)[0]

    if n_constants>0:
        if OPTIMIZE:
            fun = lambda x: eval_ind(x)
            res = minimize(fun, np.ones(n_constants), method='SLSQP',options  = {"maxiter":10, "disp":True},callback = minimize_stopper.__call__)
            opt_const = res['jac']
        else:
            opt_const = np.random.rand(n_constants)
        for index in range(n_constants):
            replace_phenotype = replace_phenotype.replace('c[' + str(index) + ']', str(opt_const[index]))
        if OPTIMIZE:
            print(replace_phenotype)
    return replace_phenotype


def setup(parameters_file_path = None):
    if parameters_file_path is not None:
        load_parameters(file_name=parameters_file_path)
    set_parameters(sys.argv[1:])
    if params['SEED'] is None:
        params['SEED'] = int(datetime.now().microsecond)
    logger.prepare_dumps()
    random.seed(params['SEED'])
    if params['ALGORITHM']=='SGE':
        grammar_sge.set_path(params['GRAMMAR'])
        grammar_sge.read_grammar()
        grammar_sge.set_max_tree_depth(params['MAX_TREE_DEPTH'])
        grammar_sge.set_min_init_tree_depth(params['MIN_TREE_DEPTH'])
    elif params['ALGORITHM']=='GE':
        params['BNF_GRAMMAR'] = grammar_ge.grammar_ge(params['GRAMMAR'])
    elif params['ALGORITHM']=='PGE':
        grammar_pge.set_path(params['GRAMMAR'])
        grammar_pge.read_grammar()

def evolutionary_algorithm(evaluation_function=None, parameters_file=None):
    setup(parameters_file_path=parameters_file)
    population = list(make_initial_population())
    it = 0
    best_overall = {}
    flag = False
    while it <= params['GENERATIONS']:
        for i in tqdm(population):
            if params['OPTIMIZE'] and it%params['OPTIMIZE_EACH'] == 0 and it!=0:
                evaluate(i, evaluation_function,OPTIMIZE=True)
            else:
                evaluate(i, evaluation_function,OPTIMIZE=False)
        population.sort(key=lambda x: x['fitness'])

        if params['ALGORITHM']=='PGE':
            if population[0]['fitness'] <= best_overall.setdefault('fitness', np.inf):
                best_overall = copy.deepcopy(population[0])
            if not flag:
                update_probs(best_overall, params['LEARNING_FACTOR'])
            else:
                update_probs(best_generation, params['LEARNING_FACTOR'])
            flag = not flag

        logger.evolution_progress(it, population)
        new_population = population[:params['ELITISM']]
        while len(new_population) < params['POPSIZE']:
            if random.random() < params['PROB_CROSSOVER']:
                p1 = tournament(population, params['TSIZE'])
                p2 = tournament(population, params['TSIZE'])
                ni = crossover(p1, p2)
            else:
                ni = tournament(population, params['TSIZE'])
            ni = mutate(ni, params['PROB_MUTATION'])
            new_population.append(ni)

        population = new_population

        if params['ALGORITHM']=='PGE':
            best_generation = copy.deepcopy(new_population[0])
            if params['ADAPTIVE']:
                params['LEARNING_FACTOR'] += params['ADAPTIVE_INCREMENT']

        it += 1

