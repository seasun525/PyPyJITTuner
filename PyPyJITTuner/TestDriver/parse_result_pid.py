import sys
import json

def parse_postgres(pid_dir):
    pid_num_list = []
    CPU_list = []
    MEM_list = []
    for key in pid_dir.keys():
        pid_list = pid_dir[key]
        temp_CPU = 0
        temp_MEM = 0
        pid_count = 0
        for pid in pid_list:
            print pid['name']
            if pid['name'] == 'postgres':
                pid_count += 1
                temp_CPU = float(pid['cpu_percent'])
                temp_MEM = float(pid['memory_info'][0])
                print pid['memory_info']
        CPU_list.append(temp_CPU)
        MEM_list.append(temp_MEM)
        pid_num_list.append(pid_count)
    return CPU_list, MEM_list, pid_num_list

def parse_worker(pid_dir, pid_ind):
    pid_num_list = []
    CPU_list = []
    MEM_list = []
    for key in pid_dir.keys():
        pid_list = pid_dir[key]
        temp_CPU = 0
        temp_MEM = 0
        pid_count = 0
        for pid in pid_list:
            print pid['ppid']
            #f pid['ppid'] == 5651:
            #print str(pid) + '#'
            if pid['ppid'] == pid_ind:
                pid_count += 1
                temp_CPU = float(pid['cpu_percent'])
                temp_MEM = float(pid['memory_info'][0])
                print pid['memory_info']
        CPU_list.append(temp_CPU)
        MEM_list.append(temp_MEM)
        pid_num_list.append(pid_count)
    return CPU_list, MEM_list, pid_num_list

def main():
    file_in_path = sys.argv[1]
    pid = int(sys.argv[2])
    file_in = open(file_in_path, 'r')
    pid_dir = json.load(file_in)
    #print parse_postgres(pid_dir)
    print parse_worker(pid_dir, pid)
    print pid
if __name__ == '__main__':
    main()
