import os
import numpy
import json

class StatLog():

    def __init__(self, output_file_dir):
        self.output_file_dir = output_file_dir
        txt_output_path = output_file_dir + '/stat_logging.txt'
        self.json_data = []
        self.gen_number = 1
        self.file_out = open(txt_output_path, 'w')

    def record_gen(self, pop):
        ind_list = []
        stat_list = []
        for ind in pop:
            ind_list.append(ind)
            stat_list.append(list(ind.fitness.values))

        vertical_stat_list = []
        for i in range(len(stat_list[0])):
            temp_list = []
            for j in range(len(pop)):
                temp_list.append(stat_list[j][i])
            vertical_stat_list.append(temp_list)


        #print statistic info to stat_logging.txt
        self.file_out.write('################  Generation %s  #################\n'%str(self.gen_number))
        self.file_out.write('object_num\tMax\tAvg\tMin\tStd\n')
        statistic_info_list = []
        for i in range(len(vertical_stat_list)):
            temp_list = []
            for j in range(len(vertical_stat_list[i])):
                temp_list.extend(list(vertical_stat_list[i][j]))
            temp_dir = {}
            temp_dir['object_num:'] = i
            temp_dir['Max'] = numpy.max(temp_list)
            temp_dir['Avg'] = numpy.average(temp_list)
            temp_dir['Min'] = numpy.min(temp_list)
            temp_dir['Std'] = numpy.std(temp_list)
            temp_list = [temp_dir['object_num:'], temp_dir['Max'], temp_dir['Avg'], temp_dir['Min'], temp_dir['Std']]
            self.file_out.write('\t'.join(map(str, temp_list))+'\n')
            self.file_out.flush()
            statistic_info_list.append(temp_dir)

        final_dir = {}
        final_dir['pop'] = ind_list
        final_dir['values'] = stat_list
        final_dir['statistics'] = statistic_info_list
        json_output = open(self.output_file_dir+'/stat_gen_'+str(self.gen_number)+'.json', 'w')
        json.dump(final_dir, json_output)
        json_output.close()
        self.gen_number += 1

        

        
