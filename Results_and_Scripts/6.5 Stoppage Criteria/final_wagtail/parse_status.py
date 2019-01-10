import json
import sys

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

def parse_resource_usage(folder):
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
    folder = sys.argv[1]
    parse_resource_usage(folder)

if __name__ == '__main__':
    main()

