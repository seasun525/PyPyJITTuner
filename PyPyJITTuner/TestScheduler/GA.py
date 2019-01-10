import subprocess
import random
import numpy
import array
import sys
import ast
import json
from deap import base
from deap import creator
from deap import tools
from deap import benchmarks

from configuration import config
from evaluation import Evaluate
from stoping import StopRule
from stat_logging import StatLog
import random
CXPB = 0.8
MUTPB = 0.1
POP_SIZE = 40

def evaluate(individual):
    Config = config()
    value_list = Config.decode_list(individual)
    y1 = value_list[0]**2+value_list[1]**2+value_list[2]**2+10
    y2 = (value_list[3]-1)**2+(value_list[4]-1)**2+15
    y3 = (value_list[5]-1)**2+20
    t_y1 = ()
    t_y2 = ()
    t_y3 = ()
    for i in range(20):
        t_y1 = t_y1 + (y1+random.random()*5,)
        t_y2 = t_y2 + (y2+random.random()*5,)
        t_y3 = t_y3 + (y3+random.random()*5,)
    return t_y1, t_y2, t_y3#, y3, y3, y3, y3, y3, y3, y3, y3, y3, y3, y3,y3,y3


def init():
    weight_tuple = tuple([-1.0]*5)
    creator.create("FitnessMax", base.Fitness, weights=weight_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 18)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selNSGA2)
    
    return toolbox, creator

def load_pop(input_file_path):
    input_file = open(input_file_path, 'r')
    lines = input_file.readlines()
    pop = []
    temp_string = ''
    flag = False
    for i in range(len(lines)):
        if flag == True:
            line = temp_string
            flag = False
        else:
            line = lines[i]

        if line.startswith('ssh '):
            individual_tuple = tuple(map(int,list(line.split(' ')[6])))
            ind = creator.Individual(individual_tuple)
            if not 'ssh' in lines[i+1]:
                individual_value = tuple(ast.literal_eval(lines[i+1].strip()))
                ind.fitness.values = individual_value
                pop.append(ind)
                i += 1
            else:
                individual_value = tuple(ast.literal_eval(lines[i+1].strip().split('ssh')[0]))
                ind.fitness.values = individual_value
                pop.append(ind)
                temp_string = 'ssh'+lines[i+1].strip().split('ssh')[1]
                flag = True
                i += 1
        if flag == False:
            i += 1
    return pop

def load_pop_from_json(input_file_path, creator):
    print input_file_path
    pop_json = json.load(open(input_file_path, 'r'))
    pop = []
    for i in range(40):
        ind = creator.Individual(tuple(pop_json['pop'][39-i]))
        ind.fitness.values = tuple(pop_json['values'][39-i])
        pop.append(ind)
    return pop


def main():
    toolbox, creator = init()
    evl = Evaluate()
    stat_log = StatLog('results/temp/')

    pop = toolbox.population(n=POP_SIZE)

    default_config_list = [0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1]
    pop[0] = creator.Individual(tuple(default_config_list))

    count = 0
    for ind in pop:
        print str(count)+' : '+','.join(map(str, ind)) 
    sys.stdout.flush()
    print len(pop)
    sys.stdout.flush()
     
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = evl.eval_pop(invalid_ind)#map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    sys.stdout.flush()
    fits = [ind.fitness.values[0] for ind in pop]

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, POP_SIZE)
    print 'selected pop size'+str(len(pop))

    sys.stdout.flush()
    pop_bef = [toolbox.clone(ind) for ind in pop]

    # Variable keeping track of the number of generations
    stat_log.record_gen(pop)
    stop_rule = StopRule()
    sys.stdout.flush()

    g = 0    
    # Begin the evolution
    while g < 20:#max(fits) < 100 and g < 10000:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        print 'TournamentDCD'+ str(len(pop))
        sys.stdout.flush()
        offspring = tools.selTournamentDCD(pop, len(pop))
        # Clone the selected individuals
        offspring = [toolbox.clone(ind) for ind in offspring]

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
        #    if random.random() < CXPB:
            toolbox.mate(child1, child2)
            if random.random() < MUTPB:
                toolbox.mutate(child1)
            if random.random() < MUTPB:
                toolbox.mutate(child2)
            del child1.fitness.values
            del child2.fitness.values

        for ind in offspring:
            print 'offspring'+' : '+','.join(map(str, ind))

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = evl.eval_pop(invalid_ind)
        print '## '+str(len(fitnesses))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop = toolbox.select(pop+offspring, POP_SIZE)
        stat_log.record_gen(pop)

        if not stop_rule.stop_criteria_all(pop_bef, pop):
            pop_bef = [toolbox.clone(ind) for ind in pop]
        else:
            break
        sys.stdout.flush()
if __name__ == '__main__':
    main()
