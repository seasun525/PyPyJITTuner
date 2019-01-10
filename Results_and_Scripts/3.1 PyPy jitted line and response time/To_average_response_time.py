import json
import ast

import sys
def get_performance_data(benchmark_file, config_index):
	print benchmark_file
	response_time_list = ast.literal_eval(open(benchmark_file, 'r').readline().split('\"')[1])
	result_list = []
	for i in range(50):
		temp_list = []
		for j in range(30):
			temp_list.append(response_time_list[config_index][0][j][i])
		result_list.append(sum(temp_list)/len(temp_list))
		print len(temp_list)
	return result_list
	#print len(response_time_list)
	#print len(response_time_list[0])
	#print len(response_time_list[0][0])
	#print len(response_time_list[0][0][0])
	
def save_as_csv(benchmark, result_list):
	print result_list
	result_dir = ''
	file_out = open(result_dir+benchmark+'_response_time_R.csv', 'w')
	for i in range(50):
		temp_list = []
		for j in range(5):
			temp_list.append(result_list[j][i])
		print temp_list
		sys.stdout.flush()
		file_out.write(','.join(map(str, temp_list))+'\n')
	file_out.close()


def main():
	benchmarks = ['html5lib', 'pidigits', 'ai', 'bm_mako', 'chaos', 'django', 'rietveld']#'bm_icbd' , 'twisted_web'

	for benchmark in benchmarks:
		benchmark_file = benchmark + '_boxplot.json'
		temp_list = []
		for i in range(5):
			data_list = get_performance_data(benchmark_file, i)
			temp_list.append(data_list)
		save_as_csv(benchmark, temp_list)

if __name__ == '__main__':
	main()



def test():
    even = 0
    oddLarge = 0
    oddSmall = 0
    c = 0
    for i in range(1000000):
        if i%2 == 1:
            even += 1
        elif i * i <= 100:
            oddSmall += 1
        elif i * i > 100 and i < 1000000:
            oddLarge += 1
        else:
            c += 3
    return c



