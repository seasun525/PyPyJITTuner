import os
import sys
import subprocess

class Dom():

    def __init__(self):
        self.threshold = 0.33
        self.p_value_threshold = 0.05
        pass

    def dominates3(self, A, B): #A, B are ind; check if A is dominated by B
        Val_A = A
        Val_B = B
        #print '##############'
        #print Val_A
        not_equal = False
        for obj_A, obj_B in zip(Val_A, Val_B):
            print(sum(obj_A)/len(obj_A))
            print(sum(obj_B)/len(obj_B))
            cliff, p_value = self.get_cliff(obj_A, obj_B)
            if p_value < self.p_value_threshold:
                if cliff > self.threshold: #A bigger than B
                    not_equal = True
                elif cliff < 0-self.threshold:
                    return False

        return not_equal

    def dominates2(self, A, B): #A, B are ind; check if A is dominated by B
        Val_A = A.fitness.values
        Val_B = B.fitness.values
        #print '##############'
        #print Val_A
        not_equal = False
        for obj_A, obj_B in zip(Val_A, Val_B):
            cliff, p_value = self.get_cliff(obj_A, obj_B)
            if p_value < self.p_value_threshold:
                if cliff > self.threshold: #A bigger than B
                    not_equal = True
                elif cliff < 0-self.threshold:
                    return False

        return not_equal

    def dominates(self, A, B): #A, B are ind; check if A is dominated by B
        Val_A = A.wvalues
        Val_B = B.wvalues

        not_equal = False
        for obj_A, obj_B in zip(Val_A, Val_B):
            cliff, p_value = self.get_cliff(obj_A, obj_B)
            if p_value < self.p_value_threshold:
                if cliff > self.threshold: #A bigger than B
                    not_equal = True
                elif cliff < 0-self.threshold:
                    return False
                
        return not_equal

    def get_cliff(self, A, B):
        CMD = ['Rscript', 'statistic.R', ','.join(map(str, A)), ','.join(map(str, B))]
        cliff_delta = 0
        #proc =  subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
        #sys.stdout = open(os.devnull, "w")
        proc_output = subprocess.check_output(' '.join(CMD), shell=True)
        
        #for line in proc_output:
        #    print line
        cliff_delta = proc_output.strip().split('"')[1].split(',')[0]
        p_value  = proc_output.strip().split('"')[1].split(',')[1]
            #break
        #proc.kill()
        #print '####'+str(cliff_delta)
        return float(cliff_delta), float(p_value)



