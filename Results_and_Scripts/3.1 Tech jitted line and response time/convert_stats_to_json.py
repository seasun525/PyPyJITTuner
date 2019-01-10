import csv
import sys
import os
import json

def main():
    benchmarks = ['db']
    index_list = [2]

    for benchmark in benchmarks:
        for index in index_list:
            response_time_list = []
            timestamp_list = []
            with open(benchmark+'_'+str(index)+'_stats.data', 'r') as csvfile:
                print csvfile.readline()
                print csvfile.readline()
                flag = True
                #line = csvfile.readline()
                for line in csvfile.readlines():
                    if not cmp(line, 'lalala\n'):
                        flag = False
                        line = csvfile.readline()
                        continue
                    if flag:
                        response_time_list.extend(map(int, line.strip().split(',')))
                    else:
                        timestamp_list.extend(map(int, line.strip().split(',')))
            print len(response_time_list)
            print len(timestamp_list)
            #for i in range(min(len(response_time_list), len(timestamp_list))):
                

if __name__ == '__main__':
    main()
