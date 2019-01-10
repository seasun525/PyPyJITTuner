import sys
import os
import time
import subprocess
from multiprocessing import Process, Manager
import random
from configuration import config

class Evaluate():

    def __init__(self):
        self.test_platform_number = 3
        self.result_dict = {}        

    def load_evaluated(self, pop):
        Config = config()
        for ind in pop:
            ind_string = Config.list_to_string(ind)
            self.result_dict[ind_string] = ind.fitness.values

    def eval_pop1(self, pop):
        eval_list = []
        
        for i in range(len(pop)/self.test_platform_number+1):
            
            temp_list = []
            #run 3 test at a time
            if i*3 + 3 < len(pop):
                temp_list = self.eval_inds(pop[i*3:i*3+3], 3)
            else:
                temp_list = self.eval_inds(pop[i*3:len(pop)], len(pop)-i*3)
            eval_list = eval_list + temp_list
        return eval_list

    def eval_pop(self, pop):
        eval_list = range(len(pop))
        Config = config()

        count = 0
        ind_count = 0
        temp_index_list = []
        for i in range(len(pop)):
            ind_string = Config.list_to_string(pop[i])
            if ind_string in self.result_dict:
                count += 1
                eval_list[i] = self.result_dict[ind_string]
            else:
                temp_index_list.append(i)
                ind_count += 1

            if ind_count == 3 or (i == len(pop)-1 and ind_count != 0):
                individual_list = [pop[x] for x in temp_index_list]
                temp_list = self.eval_inds(individual_list, ind_count)
                for j in range(ind_count):
                    eval_list[temp_index_list[j]] = temp_list[j]
                    ind_string = Config.list_to_string(pop[temp_index_list[j]])
                    self.result_dict[ind_string] = temp_list[j]
                temp_index_list = []
                ind_count = 0
        print 'Number of individuals already evaluated '+ str(count) +'\n'
        return eval_list


    def eval_inds(self, inds, num):
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read('load_test.cfg')
        TD_IP1 = config.get('LoadTest', 'TD_IP1')
        TD_IP2 = config.get('LoadTest', 'TD_IP2')
        TD_IP3 = config.get('LoadTest', 'TD_IP3')
        LG_IP1 = config.get('LoadTest', 'LG_IP1')
        LG_IP2 = config.get('LoadTest', 'LG_IP2')
        LG_IP3 = config.get('LoadTest', 'LG_IP3')

        temp_list = []
        jobs = []
        client_list = [TD_IP1, TD_IP2, TD_IP3]
        jmeter_list = [LG_IP1, LG_IP2, LG_IP3]

        manager = Manager()
        temp_dict = manager.dict()
        for i in range(num):
            p = Process(target=self.eval_ind, args=(inds[i], i, temp_dict, client_list[i], jmeter_list[i]))
            jobs.append(p)
            p.start()
            
        for proc in jobs:
            proc.join()

        for i in range(num):
            temp_list.append(temp_dict[i])
        
        return temp_list


    def eval_ind(self, ind, index, d, client, jmeter):
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read('load_test.cfg')
        driver_path = config.get('LoadTest', 'driver_path')

        Config = config()
        ind_string = Config.list_to_string(ind)
        CMD = ['ssh', 'seasun@%s'%client, '\'ALLOWED_HOSTS=\"%s\"'%client,'SECRET_KEY=\"308159\"', 'pypy', driver_path+'/run_test.py', ind_string, jmeter, '> results/temp/run_test.log 2>&1\' ']
        print 'evaluating:' + ind_string
        print ' '.join(CMD)
        proc = subprocess.Popen(' '.join(CMD), shell=True)
        proc.wait()

        CMD = ['ssh', 'seasun@%s'%client, 'cat', 'results/%s/individual_value'%ind_string]
        proc = subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
        
        result_list = []
        for line in proc.stdout:
            temp_tuple = tuple(map(float, line.strip().split(',')))
            result_list.append(temp_tuple)
        if result_list == []:
            CMD = ['ssh', 'seasun@%s'%client, 'pypy', 'parse_result_quokka.py', 'results/%s/'%ind_string]
            proc = subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
            proc.wait()
            CMD = ['ssh', 'seasun@%s'%client, 'cat', 'results/%s/individual_value'%ind_string]
            proc = subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
            for line in proc.stdout:
                temp_tuple = tuple(map(float, line.strip().split(',')))
                result_list.append(temp_tuple)
            
        FNULL = open(os.devnull, 'w')
        CMD = ['ssh', 'seasun@%s'%client, 'pypy', driver_path+'/reset_database.py']
        proc = subprocess.Popen(' '.join(CMD), shell=True, stdout=FNULL)
        proc.wait()
        
        #wait for client system restart
        time.sleep(5*60)

        #print result_list
        d[index] =  tuple(result_list)

    def eval_ind1(self, ind, index, d, client, jmeter):
        Config = config()
        value_list = Config.decode_list(ind)
        y1 = value_list[0]**2+value_list[1]**2+value_list[2]**2
        y2 = (value_list[3]-1)**2+(value_list[4]-1)**2
        y3 = (value_list[5]-1)**2
        t_y1 = ()
        t_y2 = ()
        t_y3 = ()
        for i in range(20):
            t_y1 = t_y1 + (y1+random.random()*5,)
            t_y2 = t_y2 + (y2+random.random()*5,)
            t_y3 = t_y3 + (y3+random.random()*5,)
        d[index] = (t_y1, t_y2, t_y3)
