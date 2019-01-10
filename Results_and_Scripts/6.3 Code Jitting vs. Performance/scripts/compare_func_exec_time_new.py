import json
import sys

def main():
    output_path = '../results/cProfile_diff_all.csv'
    base_config = '011011011011011011'
    configs = '110101011000100111'

    root_dir = '/home/seasun/JIT_unfriendly_func/cProfile_results/'

    base = json.load(open(root_dir+base_config+'/cProfile.json', 'r'))
    config_dict = json.load(open(root_dir+configs+'/cProfile.json', 'r'))

    jitted_methods = json.load(open('../jit_result/'+configs+'/jitted_methods.json', 'r'))

    result = {}
    for key in base.keys():
        base_time = float(base[key]['time'])
        base_count = float(base[key]['count'])
        if base_count == 0:
            continue
        base_time = base_time/base_count

        temp_time = float(config_dict[key]['time'])
        temp_count = float(config_dict[key]['count'])
        if temp_count == 0:
            continue
        temp_time = temp_time/temp_count
        diff = (temp_time-base_time)

        result[key] = diff

    output = open(output_path, 'w')
    items=result.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort()
    backitems.reverse()
    count = 0
    for value in backitems:
        if count == 30:
            break
        if value[1] in jitted_methods.keys():
            output.write(','.join(map(str, value))+'\n')
            count += 1
            print(value)
#    json.dump(result, output)
    output.close()

if __name__ == '__main__':
    main()

