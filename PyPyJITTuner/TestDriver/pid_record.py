import json
import os
import sys
import psutil
import time
import subprocess
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('load_test.cfg')

result_root_dir = config.get('LoadTest', 'result_root_dir')
jitlog_temp_dir = config.get('LoadTest', 'jitlog_temp_dir')

monitor_duration = config.getint('LoadTest', 'duration')
monitor_interval = config.getint('LoadTest', 'monitor_interval')

#file_out_path = jitlog_temp_dir+'/pid_status.csv'

def main():

    def get_status_list():
        p_list = []
        for p in psutil.process_iter():
            try:
                p = p.as_dict(['username', 'memory_info', 'cpu_percent', 'name', 'ppid'])
            except psutil.NoSuchProcess:
                pass
            else:
                p_list.append(p)
        return p_list

    start_time = time.time()
    count = 0
    pid_status_dir = {}
    while(time.time()-start_time < monitor_duration):
        pid_status_dir[count] = get_status_list()
        count += 1
        time.sleep(monitor_interval)

    file_out_path = jitlog_temp_dir + '/pid_status.json'
    file_out = open(file_out_path, 'w')
    json.dump(pid_status_dir,file_out)
    file_out.close()


if __name__ == '__main__':
    main()
