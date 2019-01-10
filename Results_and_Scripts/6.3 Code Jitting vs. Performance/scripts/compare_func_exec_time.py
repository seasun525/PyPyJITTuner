import json
import sys

def main():
    output_path = '../results/cProfile_diff_all.json'
    base_config = '011011011011011011'
    configs = ['110101011000100111', '001001010101011111', '110100011011101101', '111010001001111010']
    #configs = ['110101011000100111', '111010001001111010']
    diff_range = 0.3

    root_dir = '/home/seasun/JIT_unfriendly_func/cProfile_results/'

    base = json.load(open(root_dir+base_config+'/cProfile.json', 'r'))
    config_list = []
    for config in configs:
        temp = json.load(open(root_dir+config+'/cProfile.json', 'r'))
        config_list.append(temp)

    result = {}
    for key in base.keys():
        temp = {}
        base_time = float(base[key]['time'])
        base_count = float(base[key]['count'])
        base_time = base_time/base_count
        if base_time == 0.0:
            continue
        for i in range(4):
            temp_time = float(config_list[i][key]['time'])
            temp_count = float(config_list[i][key]['count'])
            temp_time = temp_time/temp_count
            diff = (base_time - temp_time)/base_time
            
            if diff > diff_range:
                temp[configs[i]] = 1
            elif diff < -diff_range:
                temp[configs[i]] = -1
            else:
                temp[configs[i]] = 0
        result[key] = temp

    output = open(output_path, 'w')
    json.dump(result, output)
    output.close()

if __name__ == '__main__':
    main()
