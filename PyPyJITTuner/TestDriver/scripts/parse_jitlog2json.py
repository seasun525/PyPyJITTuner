import sys
import os
from jitlog_parser import *
import io
import shutil
import json

time_list = [15, 30, 120]
worker_number = 3

def get_pid_list(result_root_dir):
    pid_list = []
    file_list = os.listdir(result_root_dir)
    for file_name in file_list:

        if file_name.startswith('gunicorn') and file_name.endswith('.jit') and not file_name.endswith('.log'):# and not file_name.endswith('.jit'):
            print file_name
            pid = file_name.split('_')[1].split('.')[0]
            pid_list.append(pid)
            print pid
    return pid_list

def get_jitlog_list(pid, result_root_dir):
    jitlog_list_dir = result_root_dir + '/gunicorn_' + pid
    jitlog_list = []
    file_list = os.listdir(jitlog_list_dir)
    for file_name in file_list: 
        jitlog_path = jitlog_list_dir + '/' + file_name
        jitlog_list.append(jitlog_path)
    return jitlog_list

def get_jitlog_path(second, jitlog_list):
    for jitlog_path in jitlog_list:
        s = jitlog_path.split('/')[-1].split('_')[2]
        
        if int(s) == second:
            print s
            return jitlog_path

    return None

def store_results(result_lists, result_root_dir):
    result_file_path = result_root_dir + '/jitlog_results.csv'

    f = open(result_file_path, 'w')
    for result_list in result_lists:
        f.write(','.join(map(str, result_list))+'\n')
    f.close()

def copy_jitlog(result_root_dir, pid):
    new_file = result_root_dir+'/gunicorn_'+str(pid)+'/gunicorn_'+str(pid)+'.jit_120_999'
    src_file = result_root_dir+'/gunicorn_'+str(pid)+'.jit'
    print new_file 
    print src_file
    shutil.copy(src_file, new_file)

def store_result_as_json(pid, result_root_dir, result_dir, t):
    output_file = result_root_dir + '/gunicorn_' + str(pid) + '/gunicorn_' + str(pid) + '_' + str(t) + '.json'
    file_out = open(output_file, 'w')
    json.dump(result_dir, file_out)
    file_out.close()

def main():
    result_root_dir = sys.argv[1]

    pid_list = get_pid_list(result_root_dir)

    parser = JitlogParser()
    result_lists = []

    for pid in pid_list[:worker_number]:

#        copy_jitlog(result_root_dir, pid)

        jitlog_list = get_jitlog_list(pid, result_root_dir)       

        temp_list = []
        last_jitted_lines = 0
        temp_list.append(int(pid))
        for t in time_list:

            result_dir = {}

            jitlog_path = get_jitlog_path(t, jitlog_list)

            if jitlog_path != None:
                print "Parsing: "+jitlog_path
                 
                result_dir = parser.get_lines_dir(jitlog_path, result_dir)

            store_result_as_json(pid, result_root_dir, result_dir, t)

def parse_test_run_log():
    result_dir = sys.argv[1]
    pid_list = get_pid_list(result_dir)
    parser = JitlogParser()
    result_lists = []
    final_dict = {}
    print pid_list
    final_output_path = result_dir+'/gunicorn_final.json'
    trace_num = 0
    for pid in pid_list:
        result_dict = {}
        print pid
        jitlog_path = result_dir+'/gunicorn_'+str(pid)+'.jit'
        output_path = result_dir+'/gunicorn_'+str(pid)+'.json'
        result_dict, trace_num_temp = parser.get_lines_dir_and_traces_num(jitlog_path, result_dict)
        trace_num += trace_num_temp
        for key in result_dict:
            if key not in final_dict:
                final_dict[key] = result_dict[key]
            else:
                for line_num in result_dict[key]:
                    if line_num not in final_dict[key]:
                        final_dict[key].append(line_num)
        file_out = open(output_path, 'w')
        json.dump(result_dict, file_out)
        file_out.close()
        result_lists.append(result_dict)
    write_trace_num = open(result_dir+'/trace_num', 'w')
    write_trace_num.write(str(trace_num/len(pid_list)))
    write_trace_num.close()
    file_out = open(final_output_path, 'w')
    json.dump(final_dict, file_out)
    file_out.close()    

def parse_test_logs(result_dir):

    #result_dir = sys.argv[1]
    pid_list = get_pid_list(result_dir)
    parser = JitlogParser()
    result_lists = []
    final_dict = {}
    final_output_path = result_dir+'/gunicorn_final.json'
    trace_num = 0
    for pid in pid_list:
        result_dict = {}
        #print pid
        jitlog_path = result_dir+'/gunicorn_'+str(pid)+'.jit'
        output_path = result_dir+'/gunicorn_'+str(pid)+'.json'
        
        result_dict, trace_num_temp = parser.get_lines_dir_and_traces_num(jitlog_path, result_dict)
        if result_dict == 0:
            continue
        trace_num += trace_num_temp
        for key in result_dict:
            if key not in final_dict:
                final_dict[key] = result_dict[key]
            else:
                for line_num in result_dict[key]:
                    if line_num not in final_dict[key]:
                        final_dict[key].append(line_num)
        file_out = open(output_path, 'w')
        json.dump(result_dict, file_out)
        file_out.close()
        result_lists.append(result_dict)
    write_trace_num = open(result_dir+'/trace_num', 'w')
    write_trace_num.write(str(trace_num/len(pid_list)))
    write_trace_num.close() 
    file_out = open(final_output_path, 'w')
    json.dump(final_dict, file_out)
    file_out.close()
 
def parse_individual_log():
    jitlog_path = sys.argv[1]
    output_path = sys.argv[2]
    result_dir = {}
    parser = JitlogParser()
    result_dir = parser.get_lines_dir(jitlog_path, result_dir)
    file_out = open(output_path, 'w')
    json.dump(result_dir, file_out)
    file_out.close()

if __name__ == '__main__':
    input_dir = sys.argv[1]
    parse_test_logs(input_dir)
