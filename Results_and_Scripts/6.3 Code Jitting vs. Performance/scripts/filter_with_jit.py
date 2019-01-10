import json
import sys
def main():
    config = sys.argv[1]
    jit_log_path = '../jit_result/'+config+'/gunicorn_final.json'
    trace_path = '../Trace_result/trace.json'
    output_path = '../jit_result/'+config+'/jitted_methods.json'

    trace = json.load(open(trace_path, 'r'))
    jit = json.load(open(jit_log_path, 'r'))

    result = {}
    jit_keys = map(str, jit.keys())
    for key in trace.keys():
        file_path = key.strip().split('==')[2]
        
        if file_path in jit_keys:
            temp = []
            for line in trace[key]:
                try:
                    if int(line) in map(int, jit[file_path]):
                        temp.append(line)
                except ValueError:
                    pass
            if not temp == []:
                result[key] = {'trace':trace[key], 'jit':temp}

    output = open(output_path, 'w')
    json.dump(result, output)
    output.close()
    

if __name__ == '__main__':
    main()
