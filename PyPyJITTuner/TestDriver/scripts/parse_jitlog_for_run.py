import csv
import sys
import os
import subprocess
import json
from parse_jitlog2json import *
from measure_coverage import *

def get_test_list(result_dir):
    item_list = os.listdir(result_dir)
    temp_list = []
    for item in item_list:
        if all(c in '01' for c in item):
            temp_list.append(result_dir+item)
    item_list = temp_list
    folder_list = []
    for item in item_list:
        if os.path.isdir(item):
            folder_list.append(item)
    return folder_list

def get_mem_info(result_dir):
    file_in = open(result_dir+'/resource_usage.csv', 'r')
    line = file_in.readlines()[-1].strip()
    return line


def get_log_info(result_dir):

    file_in = open(result_dir + '/line_coverage')
    coverage = file_in.readline().strip()
    file_in.close()
    ind_string = result_dir.split('/')[-1]
    return ind_string+','+coverage+','+get_mem_info(result_dir)+'\n'
    
def get_coverage_measurement(result_dir, profile_dict):
    jit_dict = load_json(result_dir+'/gunicorn_final.json')
    
    profiled_covered_line = get_number_of_lines(jit_dict)
    write_line_num = open(result_dir+'/line_coverage', 'w')
    write_line_num.write(str(profiled_covered_line))# +','+ str(not_profiled_covered_line))
    write_line_num.close()

def check_parsed(result_dir):
    item_list = os.listdir(result_dir)
    if 'line_coverage' in item_list:
        return True
    else:
        return False 

def get_resource_by_name(name, data_dic):
    CPU_list = []
    MEM_list = []
    for i in range(len(data_dic)):
        pid_status_snapshot = data_dic[str(i)]
        temp_CPU = 0.0
        temp_MEM = 0.0
        for j in range(len(pid_status_snapshot)):
            if pid_status_snapshot[j]['name'] == name:
                temp_CPU += pid_status_snapshot[j]['cpu_percent']
                temp_MEM += pid_status_snapshot[j]['memory_info'][0]
        CPU_list.append(temp_CPU)
        MEM_list.append(temp_MEM)
    return [CPU_list, MEM_list]

def get_resource_by_ppid(ppid, data_dic):
    CPU_list = []
    MEM_list = []
    for i in range(len(data_dic)):
        pid_status_snapshot = data_dic[str(i)]
        temp_CPU = 0.0
        temp_MEM = 0.0
        for j in range(len(pid_status_snapshot)):
            if pid_status_snapshot[j]['ppid'] == ppid:
                temp_CPU += pid_status_snapshot[j]['cpu_percent']
                temp_MEM += pid_status_snapshot[j]['memory_info'][0]
        CPU_list.append(temp_CPU)
        MEM_list.append(temp_MEM)
    return [CPU_list, MEM_list]

def get_pid_list(result_root_dir):
    pid_list = []
    file_list = os.listdir(result_root_dir)
    for file_name in file_list:

        if file_name.startswith('gunicorn') and file_name.endswith('.jit') and not file_name.endswith('.log'):# and not file_name.endswith('.jit'):
            #print file_name
            pid = file_name.split('_')[1].split('.')[0]
            pid = int(pid)
            pid_list.append(pid)
            #print pid
    return pid_list

def parse_resource_usage(folder):
    pid_list = get_pid_list(folder)
    file_in_path = folder+'/pid_status.json'
    file_in = open(file_in_path, 'r')
    data_dic = json.load(file_in)
    worker_usage_list = get_resource_by_name('pypy', data_dic)#get_resource_by_ppid(min(pid_list), data_dic)
    postgres_usage_list = get_resource_by_name('postgres', data_dic)

    file_out_path = folder + '/resource_usage.csv'
    file_out = open(file_out_path, 'w')
    file_out.write('Time, W_CPU, W_MEM, D_CPU, D_MEM\n')
    for i in range(min(len(worker_usage_list[0]),len(postgres_usage_list[0]))):
        temp_list = [i,worker_usage_list[0][i], worker_usage_list[1][i], postgres_usage_list[0][i],postgres_usage_list[1][i]]
        file_out.write(','.join(map(str, temp_list))+'\n')
    file_out.close()


def main():
    result_dir = sys.argv[1]
    folder_list = get_test_list(result_dir)
    print folder_list
    profile_dict = {}
    for folder in folder_list:
        print 'parseing: '+folder
        sys.stdout.flush()
        if check_parsed(folder) == True:
            continue
        parse_resource_usage(folder)
        parse_test_logs(folder)
        get_coverage_measurement(folder, profile_dict)
    final_output = open(result_dir+'/coverage.csv', 'w')

    for folder in folder_list:
        try:
            final_output.write(get_log_info(folder))
        except IOError:
           continue
    final_output.close()       
    print 'done'

if __name__ == '__main__':
    main() 
