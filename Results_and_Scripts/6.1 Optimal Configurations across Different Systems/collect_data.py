import sys
import subprocess
import json
import os

def get_test_runs(d):
    test_runs = [name for name in os.listdir(d) if os.path.isdir(d+name)]
    print test_runs
    return test_runs

def collect_data(test_dir):
    file_in = open(test_dir+'line_coverage','r')
    jitted_line_num = file_in.readline().split(',')[0]
    
    response_time_list = []
    file_in = open(test_dir+'individual_value')
    for line in file_in.readlines():
        value_list = map(int, line.strip().split(','))
        avg_value = sum(value_list)/len(value_list)
        response_time_list.append(avg_value)

    response_time_list.append(sum(response_time_list))
    return str(jitted_line_num)+','+','.join(map(str, response_time_list))

def main():
    root_dir = '/mnt/SCALEDISK02/Yangguang/'
    file_out = open(root_dir+'quokka_jitted_response.csv', 'w')
    machines = ['scale05', 'scale06', 'scale08']
    for machine in machines:
        test_runs_dir = root_dir + machine + '/quokka_second_run/'
        test_runs = get_test_runs(test_runs_dir)
        for test in test_runs:
            test_dir = test_runs_dir + test + '/'
            #if not os.path.exists(test_dir+'gunicorn_traces_final.json'):
            #    print test_dir
            #parse_test_run(test_dir)
            try:
                line = collect_data(test_dir)
            except IOError:
                print test_dir
                continue
            line = test + ',' + line + '\n'
            file_out.write(line)

    file_out.close()

if __name__ == '__main__':
    main()
