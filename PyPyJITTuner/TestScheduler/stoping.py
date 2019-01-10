import subprocess
from dominate import Dom

class StopRule():

    def __init__(self):
        self.criteria_1 = False
        self.criteria_2 = False
        self.criteria_3 = False
        self.criteria_4 = False
        self.criteria_first_1 = False
        self.criteria_first_2 = False
        self.criteria_first_3 = False
        self.criteria_first_4 = False
        self.D = Dom()

    def stop_criteria_1(self, pop_bef, pop_aft):
        pass

    def dom_pop(self, pop1, pop2):
        count = 0
        for ind1 in pop1:
            for ind2 in pop2:
                if self.D.dominates2(ind1, ind2):
                    count += 1
                    break
        return count

    def dom_ind(self, ind1, ind2):
        fit1 = ind1.fitness.values
        fit2 = ind2.fitness.values
        for i in range(len(fit1)):
            if fit1[i] > fit2[i]:
                return False
        return True

    def measure_MDR(self, pop_bef, pop_aft):
        dom_A_B = self.dom_pop(pop_bef, pop_aft)
        dom_B_A = self.dom_pop(pop_aft, pop_bef)
        MDR = float(dom_A_B)/len(pop_bef) - float(dom_B_A)/len(pop_aft)
        print 'dom_A_B:\t'+str(float(dom_A_B))
        print 'dom_B_A:\t'+str(float(dom_B_A))
        print 'MDR:\t'+str(abs(MDR))
        return abs(MDR)


    def T_test(self, pop_bef, pop_aft):
        value_list = []
        result_list_bef = []
        for i in range(len(pop_bef[0].fitness.values)):
            temp_list = []
            for j in range(len(pop_bef)):
                temp_list.append(pop_bef[j].fitness.values[i])
            result_list_bef.append(temp_list)

        result_list_aft = []
        for i in range(len(pop_aft[0].fitness.values)):
            temp_list = []
            for j in range(len(pop_aft)):
                temp_list.append(pop_aft[j].fitness.values[i])
            result_list_aft.append(temp_list)

        for i in range(len(result_list_bef)):
            value_list.append(self.cal_t_value(result_list_bef[i], result_list_aft[i]))

        for val in value_list:
            if val > 0.05:
                return False, value_list
        return True, value_list

    def cal_t_value(self, list1, list2):
        CMD = ['python', 'T_test.py', '\''+','.join(map(str, list1))+'\'', '\''+','.join(map(str, list2))+'\'']
        proc = subprocess.Popen(' '.join(CMD), stdout=subprocess.PIPE, shell=True)
        result_list = []
        for line in proc.stdout:
            result_list = line.strip().split(' ')
            break
        return float(result_list[1])

    def stop_criteria_all(self, pop_bef, pop_aft):
        MDR = self.measure_MDR(pop_bef, pop_aft)
        if MDR < 0.5 and self.criteria_2 == False:
            if self.criteria_first_2 == False:
                self.criteria_first_2 = True
            else:
                self.criteria_2 = True
        else:
            self.criteria_first_2 = False

        #criteria 2
        if MDR < 0.25 and self.criteria_3 == False:
            if self.criteria_first_3 == False:
                self.criteria_first_3 = True
            else:
                self.criteria_3 = True
        else:
            self.criteria_first_3 = False

        #criteria 3
        if MDR < 0.1 and self.criteria_4 == False:
            if self.criteria_first_4 == False:
                self.criteria_first_4 = True
            else:
                self.criteria_4 = True
        else:
            self.criteria_first_4 = False

        print 'MDR is: '+str(MDR)
        print 'Criteria 1: '+str(self.criteria_2)
        print 'Criteria 2: '+str(self.criteria_3)
        print 'Criteria 3: '+str(self.criteria_4)

        if self.criteria_2 and self.criteria_3 and self.criteria_4:
            return True
        else:
            return False

