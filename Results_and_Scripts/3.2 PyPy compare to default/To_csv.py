import json
import ast

def get_warmup_iter(benchmark):
	jitted_line_file = benchmark + '_jitted_line.csv'
	file_in = open(jitted_line_file, 'r')
	warmup_iter_list = []
	lines = file_in.readlines()
	for line in lines:
		temp_list = lines[2].strip().split(',')
		warmup_iter = temp_list.index(temp_list[-1])
		warmup_iter_list.append(warmup_iter)
	return warmup_iter_list

def get_performance_data(benchmark, last_iterations):
	benchmark_file = benchmark + '_boxplot.json'
	warmup_iter_list = get_warmup_iter(benchmark)
	response_time_list = ast.literal_eval(open(benchmark_file, 'r').readline().split('\"')[1])
	result_list = []
	for config_index in range(6):#[0,1,3,5,8,11]:
		#print [0,1,3,5,8,11].index(config_index)
		temp_list = []
		for run_number in range(5):
			for j in range(30):
				temp_list.append(response_time_list[config_index][0][run_number][-(j+1)])
		result_list.append(temp_list)
		print len(temp_list)
	return result_list
	#print len(response_time_list)
	#print len(response_time_list[0])
	#print len(response_time_list[0][0])
	#print len(response_time_list[0][0][0])
	
def save_as_csv(benchmark, result_list):
	for config_index in range(6):#[0,1,3,5,8,11]:#
		file_out = open(benchmark+'_'+str(5+config_index)+'_performance_data.csv', 'w')
		#for i in range(len(result_list[0])):
		#	temp_list = []
		#	for j in range(5):
		#		temp_list.append(result_list[j][i])
		file_out.write('\n'.join(map(str, result_list[config_index])))
		file_out.close()

def main():
	benchmarks = ['pidigits']#'bm_icbd' , 'twisted_web'
	warmup_iterations = [34,29,10,11,42,11,0]
	for benchmark in benchmarks:
		
		data_list = get_performance_data(benchmark, benchmarks.index(benchmark))
		save_as_csv(benchmark, data_list)

if __name__ == '__main__':
	main()