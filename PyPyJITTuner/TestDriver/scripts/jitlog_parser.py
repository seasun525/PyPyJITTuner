import sys
from jitlog import parser
import os
sys.path.append('vmprof-server/vmlog')
from serializer import *

class JitlogParser():
    
    def get_lines(self, file_name):
        line_number = []
        print file_name
        f = parser.parse_jitlog(file_name)
        lSerializer = LogMetaSerializer()
        d = lSerializer.to_representation(f)
        tSerializer = TraceSerializer()
        f.extract_source_code_lines()

        for i in f.traces:
            print 'trace:' + str(i) + 'SSSSSSSSSSSSSSSS'
            dic = tSerializer.to_representation(f.traces[i])
            code_dic = dic['code']
            print code_dic
            for key in code_dic:
                code_file_dic = code_dic[key]
                for key1 in code_file_dic:
                    if key1 not in line_number:
                        line_number.append(key1)
        return len(line_number)

    def get_lines_dir(self, file_name, result_dir):
        line_number = []
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
            #print 'OOOOOOOOOOOOOOOOOOLLLLLLLL'+code_dic
            for key in code_dic:
                code_file_dic = code_dic[key]
#               print 'MMMMMMMMMMMMMMMMMMM'+key

                if key in result_dir.keys():
                    line_list = result_dir[key]
                else:
                    line_list = []

                for key1 in code_file_dic:
                    if key1 not in line_list:
                        #print 'MMMMMMMMMMMMMMMMMMM'+str(key1)
                        line_list.append(key1)
 
                result_dir[key] = line_list
        return result_dir

    def get_lines_dir_and_traces_num(self, file_name, result_dir):
        line_number = []
        print file_name
        try:
            f = parser.parse_jitlog(file_name)
        except parser.ParseException:
            return 0,0
        lSerializer = LogMetaSerializer()
        d = lSerializer.to_representation(f)
        tSerializer = TraceSerializer()
        #try:
        f.extract_source_code_lines()
        #except IndexError:
        #    return 0,0
        for i in f.traces:
            #print 'trace:' + str(i) + 'SSSSSSSSSSSSSSSS'
            dic = tSerializer.to_representation(f.traces[i])
            code_dic = dic['code']
            #print 'OOOOOOOOOOOOOOOOOOLLLLLLLL'+code_dic
            for key in code_dic:
                code_file_dic = code_dic[key]
#               print 'MMMMMMMMMMMMMMMMMMM'+key

                if key in result_dir.keys():
                    line_list = result_dir[key]
                else:
                    line_list = []

                for key1 in code_file_dic:
                    if key1 not in line_list:
                        #print 'MMMMMMMMMMMMMMMMMMM'+str(key1)
                        line_list.append(key1)

                result_dir[key] = line_list
        return result_dir, len(f.traces)
