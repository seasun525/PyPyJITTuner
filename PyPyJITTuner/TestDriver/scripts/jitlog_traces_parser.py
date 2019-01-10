import sys
from jitlog import parser
import os
sys.path.append('vmprof-server/vmlog')
from serializer import *

class JitlogParser():
    
    ###
    # parse a jitlog from 'file_name'
    # combine the results to 'result_dir' which is a dictionary.
    ###
    def get_traces_dir(self, file_name, result_dir):
        liine_number = []
        print file_name
        f = parser.parse_jitlog(file_name)
        lSerializer = LogMetaSerializer()
        d = lSerializer.to_representation(f)
        tSerializer = TraceSerializer()
        f.extract_source_code_lines()
        for i in f.traces:
            #print 'trace:' + str(i) + 'SSSSSSSSSSSSSSSS'
            dic = tSerializer.to_representation(f.traces[i])
            code_dic = dic['code']
            print dic#.keys() 
             

            temp_trace = {}
            for key in code_dic:
                code_file_dic = code_dic[key]
                temp_trace[key] = code_file_dic.keys()
            for key in temp_trace:
                
                if key in result_dir.keys():
                    trace_list = result_dir[key]
                else:
                    trace_list = []

                temp = {}
                if len(temp_trace.keys()) > 1:
                    temp['flag'] = 1
                else:
                    temp['flag'] = 0
                temp['trace'] = temp_trace

                if temp not in trace_list:
                    trace_list.append(temp)

                result_dir[key] = trace_list

        return result_dir
