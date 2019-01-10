import json
import sys
import os

root_dir = ''

def get_test_list(root_dir):
    l = os.listdir(root_dir)
    temp = []
    for ll in l:
        if os.path.isdir(root_dir+'/'+ll):
            temp.append(ll)
    return temp

def get_jitted_line_num(test_dir):
    jit_input = test_dir + '/gunicorn_final.json'
    j = json.load(open(jit_input, 'r'))
    counter = 0
    for key in j.keys():
        counter += len(j[key])
    return counter

def get_response_time_list(test_dir):
    read_lines = open(test_dir+'/individual_value', 'r').readlines()
    response_time_list = []

    for i in range(12):
        line = read_lines[i]
        response_times = map(int, line.strip().split(','))
        avg = sum(response_times)/len(response_times)
        response_time_list.append(avg)

    return response_time_list

def main():
    #est_list = get_test_list(root_dir)

    test_list = ['111111000111111001', '111111001111111001', '110111001010111011','110111001100111011','110111001110111011','111111001000111011', '111111001110111011']
    test_result_list = []
    for l in test_list:
        test_dir = root_dir+'/'+l
        jitted_line_num = get_jitted_line_num(test_dir)
        response_time = get_response_time_list(test_dir)
        temp = [l]+[jitted_line_num]+response_time
        test_result_list.append(temp)

    output = open(root_dir+'/'+'jitted_line_responsetime.csv', 'w')
    for t in test_result_list:
        output.write(','.join(map(str, t))+'\n')
    output.close()


if __name__ == '__main__':
    main()
