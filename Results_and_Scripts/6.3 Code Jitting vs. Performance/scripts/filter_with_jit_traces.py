import json
import sys
def main():
    config = sys.argv[1]
    jit_log_path = '../jit_result/'+config+'/gunicorn_traces_final.json'
    trace_path = '../Trace_result/trace.json'
    output_path = '../jit_result/'+config+'/jitted_methods_traces.json'

    trace = json.load(open(trace_path, 'r'))
    jit = json.load(open(jit_log_path, 'r'))

    result = {}
    jit_keys = map(str, jit.keys())
    for key in trace.keys():
        file_path = key.strip().split('==')[2]

        temp_jitted_traces = []        
        if file_path in jit_keys:
            try:
                traced_lines = map(int, trace[key])
            except ValueError:
                traced_lines = []
                for line in trace[key]:
                    if line.isdigit():
                        traced_lines.append(line) 
            for jitted_trace in jit[file_path]:
                
                jitted_lines = map(int, jitted_trace['trace'][file_path])
                for jitted_line in jitted_lines:
                    if jitted_line in traced_lines:
                        if jitted_trace not in temp_jitted_traces:
                            temp_jitted_traces.append(jitted_trace)
                            break

        if not temp_jitted_traces == []:
            result[key] = {'trace':trace[key], 'jitted_trace':temp_jitted_traces}
        else:
            result[key] = {'trace':trace[key], 'jitted_trace':[]}

    output = open(output_path, 'w')
    json.dump(result, output)
    output.close()
    

if __name__ == '__main__':
    main()
