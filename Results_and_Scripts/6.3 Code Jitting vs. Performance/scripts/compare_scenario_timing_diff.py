import json
import sys

def main():
    configs = ['001001010101011111',  '110100011011101101',  '111010001001111010', '110101011000100111']
    base = '011011011011011011'
    response_time_list = []
    for config in configs:
        temp_list = []
        file_in = open('../cProfile_results/'+config+'/individual_value', 'r')
        lines = file_in.readlines()
        for line in lines:
            l = map(int,line.strip().split(','))
            temp_list.append(sum(l)/len(l))
        response_time_list.append(temp_list)


    base_time_list = []
    file_in = open('../cProfile_results/'+base+'/individual_value', 'r')
    lines = file_in.readlines()
    for line in lines:
        l = map(int,line.strip().split(','))
        base_time_list.append(sum(l)/len(l))


    for i in range(12):
        diff = 0
        flag = 0
        for config in configs:
            base_time = base_time_list[i]
            response_time = response_time_list[configs.index(config)][i]
            temp_diff = float(response_time - base_time)/float(base_time)
            print config + ":" + str(response_time)
            if temp_diff > diff:
                diff = temp_diff
                flag = configs.index(config)
        break
        print 'scenario:'+str(i)+'\tdiff:'+str(diff) + 'config:' + configs[flag]

if __name__ == '__main__':
    main()
