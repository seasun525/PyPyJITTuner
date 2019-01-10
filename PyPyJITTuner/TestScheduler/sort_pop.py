from deap import tools
from deap import creator
from deap import base
import random
import numpy
import array
import json
import subprocess

object_num = 12

def get_ind_list():
    ind_list = []
    for client in client_list:
        CMD = ['ssh', 'seasun@%s'%client, 'ls', 'results/']
        proc = subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
        for line in proc.stdout:
            ind_list.append(line.strip())

    return ind_list


def get_ind_value(ind, clients):
    ind_string = ''.join(map(str, ind))
    result_list = []
    Flag = False
    for client in clients:

        CMD = ['ssh', 'seasun@%s'%client, 'cat', 'results/%s/individual_value'%ind_string]
        proc = subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
        for line in proc.stdout:
            Flag = True
            temp_tuple = tuple(map(float, line.strip().split(',')))
            result_list.append(temp_tuple)
	if Flag == True:
            break
    #print result_list
    if Flag == False:
        print(ind_string+'+++++++++++++++++++++++++++')
        return False
    return result_list

def main():
    weight_tuple = tuple([-1.0]*object_num)
    creator.create("FitnessMax", base.Fitness, weights=weight_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 18)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selNSGA2)

    import ConfigParser
    config = ConfigParser.RawConfigParser()
    config.read('load_test.cfg')
    TD_IP1 = config.get('LoadTest', 'TD_IP1')
    TD_IP2 = config.get('LoadTest', 'TD_IP2')
    TD_IP3 = config.get('LoadTest', 'TD_IP3')

    client_list = [TD_IP1, TD_IP2, TD_IP3]

    pop = []
    ind_list = get_ind_list()
    print(len(ind_list))
    for ind_string in ind_list:
        individual_value = get_ind_value(ind_string, client_list)
        if individual_value == False:
            continue
        ind = creator.Individual(tuple(map(int, list(ind_string))))
        ind.fitness.values = tuple(individual_value)
        pop.append(ind)
    print(len(pop))

    pop_bef = pop
    for i in range(5):
        ind = pop[i]
        ind_string = ''.join(map(str,ind))
        print ind_string
    pop = toolbox.select(pop, len(pop))

    temp_directory = 'results/top_configs'
    for i in range(5):
        ind = pop[i]
        ind_string = ''.join(map(str,ind))
        print ind_string
        result_tuple = ind.fitness.values
        file_out = open(temp_directory+'/tops/'+str(i)+'_'+ind_string, 'w')
        for values in result_tuple:
            file_out.write(','.join(list(map(str,values)))+'\n')
        file_out.close()
    
if __name__ == '__main__':
    main()
