import json
import sys
from colored import fg, bg, attr

def main():
    flag = int(sys.argv[1])

    if flag == 1:
        config = '111010001001111010'
    else:
        config = '110101011000100111'
    jitted_methods = json.load(open('../jit_result/'+config+'/jitted_methods.json', 'r'))
    #onfig2 = '001001010101011111'
    #itted_methods2 = json.load(open('../jit_result/'+config2+'/jitted_methods.json', 'r'))

    jitted_traces = json.load(open('../jit_result/'+config+'/jitted_methods_traces.json', 'r'))
    #itted_traces2 = json.load(open('../jit_result/'+config2+'/jitted_methods_traces.json', 'r'))
 
    key = sys.argv[2]
    file_name = key.split('==')[2]
    try:
        jitted = jitted_methods[key]['jit']
        profiled = jitted_methods[key]['trace']
        traces = jitted_traces[key]['jitted_trace']
    except KeyError:
        print 'Key error ++++++++++++++'
        exit()
        #itted = jitted_methods2[key]['jit']
        #rofiled = jitted_methods2[key]['trace']

    jitted = map(int, jitted)
    profiled = map(int, profiled)

    file_in = open(file_name, 'r')
    lines = file_in.readlines()

    for i in range(min(profiled)-10, max(profiled)+10):
        if i not in range(len(lines)):
            return
        if i == 226:
            print ('\t\t%s %s %s' % (fg(2), '......', attr(0)))
        if i in profiled:
            if i in jitted:
                print (str(i)+' %s %s %s' % (fg(11), lines[i-1].split('\n')[0], attr(0)))
            else:
                print (str(i)+' %s %s %s' % (fg(2), lines[i-1].split('\n')[0], attr(0)))
        else:
            print(str(i)+' '+lines[i-1].split('\n')[0])
        
    jitted_traces = jitted_traces[key]['jitted_trace']
    count = 0
    line_counter = 0
    for trace in jitted_traces:
#        print "###############"+str(count)
        count += 1
        for f in trace['trace'].keys():
            line_counter += len(trace['trace'][f])
#            print f + ':' + ','.join(map(str, trace['trace'][f]))
    print 'average is:' + str(line_counter/count)

if __name__ == '__main__':
    main()

