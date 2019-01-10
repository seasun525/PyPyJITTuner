import json
import sys

def check_if_jitted(d, key):
    if key in d.keys():
        return True
    return False


def main(num):
    output_path = '../results/scenario_'+str(num)+'_diff_all'+'.csv'
    configs = ['110101011000100111', '001001010101011111', '110100011011101101', '111010001001111010']
#    configs = ['110101011000100111']
    func_diff = json.load(open('../results/cProfile_diff_all.json', 'r'))
    ranked_cprofile_funcs = json.load(open('/home/seasun/JIT_unfriendly_func/cProfile_results/011011011011011011/cProfile.json', 'r'))
    ranked2 = json.load(open('/home/seasun/JIT_unfriendly_func/cProfile_results/110101011000100111/cProfile.json', 'r'))
    jit_root_dir = '/home/seasun/JIT_unfriendly_func/jit_result/'
    jit_dict = {}
    for config in configs:
        temp = json.load(open(jit_root_dir+config+'/jitted_methods.json', 'r'))
        jit_dict[config] = temp

    trace_for_scenario = json.load(open('../Trace_result/results/'+str(num)+'_requst.json'))
    scenario_keys = trace_for_scenario.keys()

    result = []
    for key in ranked_cprofile_funcs.keys():
#        print key
        if 'Call  '+key not in scenario_keys:
            continue
        func = ranked_cprofile_funcs[key]
        time = func['time']
        time2 = ranked2[key]['time']
        count = func['count']
        count2 = ranked2[key]['count']
        if key not in func_diff.keys():
            continue
        diff = func_diff[key]
        #G_J, G_N, B_J, B_N, N_J, N_N
        temp_counter = [0,0,0,0,0,0]



        for config in diff.keys():
            difference = diff[config]
            jitted = check_if_jitted(jit_dict[config], key)
            if difference == 1 and jitted:
                temp_counter[0]+=1
            elif difference == 1 and not jitted:
                temp_counter[1]+=1
            elif difference == -1 and jitted:
                temp_counter[2]+=1
            elif difference == -1 and not jitted:
                temp_counter[3]+=1
            elif difference == 0 and jitted:
                temp_counter[4]+=1
            elif difference == 0 and not jitted:
                temp_counter[5]+=1
        temp_dict = {}
        temp_dict['key'] = key
        temp_dict['time'] = time
        temp_dict['time2'] = time2
        temp_dict['count'] = count
        temp_dict['count2'] = count2
        temp_dict['avg'] = float(time)/float(count)
        temp_dict['avg2'] = float(time2)/float(count2)
        if float(time2)/float(count2) != 0:
            temp_dict['diff'] = (float(time)/float(count)-float(time2)/float(count2))/(float(time)/float(count))
        else:
            temp_dict['diff'] = 0
        temp_dict['value'] = temp_counter
        result.append(temp_dict)

    output = open(output_path, 'w')
    output.write('function,diff,time,count,avg,time2,count2,avg2,Good_J,Good_NJ,Bad_J,Bad_NJ,Nat_J,Nat_NJ\n')
    for counter in result:
        line = counter['key']+','+str(counter['diff'])+','+counter['time']+','+str(counter['count'])+','+str(counter['avg'])+','+counter['time2']+','+str(counter['count2'])+','+str(counter['avg2'])+','+','.join(map(str, counter['value'])) + '\n'
        output.write(line)
    output.close()

if __name__ == '__main__':
    for i in range(13):
        main(i)
