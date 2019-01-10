import json
import sys
import pstats

def temp():
    input_path = sys.argv[1]

    p = pstats.Stats(input_path)
    p.sort_stats('time')
    p.print_stats()

def parse_line(line):
    splits = line.split()
    tottime = splits[1]
    if splits[0].isdigit():
        count = int(splits[0])
    else:
        count = int(splits[0].split('/')[0])
    file_func = ' '.join(splits[5:])
    if '}' in file_func:
        return {}
    else:
        file_name = file_func.split(':')[0]
        line = file_func.split(':')[1].split('(')[0]
        func_name = file_func.split('(')[1].split(')')[0]

    temp_dict = {}
    temp_dict['func_name'] = func_name
    temp_dict['file_name'] = file_name
    temp_dict['time'] = tottime
    temp_dict['count'] = count
    temp_dict['line'] = int(line)
    key = func_name + '==' + line + '==' + file_name
    temp_dict['key'] = key
    return temp_dict
   
def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    lines = open(input_path, 'r').readlines()
    temp_list = []
    for line in lines[8:-2]:
        if len(line) > 10:
            d = parse_line(line)
            if d != {}:
                key = d['key']
                temp_list.append(d)
                #temp_list[key] = d

    output_stream = open(output_path,'w')
    json.dump(temp_list, output_stream)
    output_stream.close()
 
if __name__ == '__main__':
    main()
