import json
import ast


def get_performance_data(benchmark_file, last_iterations):
	response_time_list = ast.literal_eval(open(benchmark_file, 'r').readline().split('\"')[1])
	result_list = []
	for config_index in range(5):
		temp_list = []
		for run_number in range(30):
			for j in range(last_iterations):
				temp_list.append(response_time_list[config_index][0][run_number][-(j+1)])
		result_list.append(temp_list)
		print len(temp_list)
	print len(response_time_list)
	print len(response_time_list[0])
	print len(response_time_list[0][0])
	print len(response_time_list[0][0][0])
	return result_list
	#print len(response_time_list)
	#print len(response_time_list[0])
	#print len(response_time_list[0][0])
	#print len(response_time_list[0][0][0])
def get_performance_data2(benchmark_file, first_iterations):
	response_time_list = ast.literal_eval(open(benchmark_file, 'r').readline().split('\"')[1])
	result_list = []
	for config_index in range(5):
		temp_list = []
		for run_number in range(30):
			for j in range(first_iterations):
				temp_list.append(response_time_list[config_index][0][run_number][j])
		result_list.append(temp_list)
		print len(temp_list)
	return result_list

def save_as_csv(benchmark, result_list):
	file_out = open(benchmark+'_warming_up.csv', 'w')
	for i in range(len(result_list[0])):
		temp_list = []
		for j in range(5):
			temp_list.append(result_list[j][i])
		file_out.write(','.join(map(str, temp_list))+'\n')
	file_out.close()

def save_as_csv2(benchmark, result_list):
	file_out = open(benchmark+'_warmed_up.csv', 'w')
	for i in range(len(result_list[0])):
		temp_list = []
		for j in range(5):
			temp_list.append(result_list[j][i])
		file_out.write(','.join(map(str, temp_list))+'\n')
	file_out.close()

def main():
	benchmarks = ['ai', 'bm_mako', 'chaos', 'django', 'rietveld', 'html5lib', 'pidigits']#'bm_icbd' , 'twisted_web'
	last_iterations = [2,2,2,2, 2, 2, 2]
	warmup_iterations = [34,29,10,11,42,11,1]

	for benchmark in benchmarks:
		benchmark_file = benchmark + '_boxplot.json'
		iteration = warmup_iterations[benchmarks.index(benchmark)]
		data_list = get_performance_data(benchmark_file, 50-iteration)
		save_as_csv(benchmark, data_list)
		data_list = get_performance_data2(benchmark_file, iteration)
		save_as_csv2(benchmark, data_list)

if __name__ == '__main__':
	main()