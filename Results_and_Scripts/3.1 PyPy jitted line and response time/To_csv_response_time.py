import json
import ast


def get_performance_data(benchmark_file, config_index):
	response_time_list = ast.literal_eval(open(benchmark_file, 'r').readline().split('\"')[1])
	result_list = []
	for i in range(30):
		temp_list = []
		for j in range(50):
			
			temp_list.append(response_time_list[config_index][0][i][j])
		result_list.append(temp_list)
		print len(temp_list)
	return result_list
	#print len(response_time_list)
	#print len(response_time_list[0])
	#print len(response_time_list[0][0])
	#print len(response_time_list[0][0][0])
	
def save_as_csv(benchmark, result_list, i):
	file_out = open(benchmark+'_'+str(i)+'_response_time.csv', 'w')
	for i in range(30):
		temp_list = result_list[i]
		file_out.write(','.join(map(str, temp_list))+'\n')
	file_out.close()

def convert_jitted_line(benchmark):
	file_in = open(benchmark+'_jitted_line.csv', 'r')
	jit_list = []
	for line in file_in.readlines():
		temp_list = line.strip().split(',')
		jit_list.append(temp_list)

	file_out = open(benchmark+'_jitted_line_R.csv', 'w')
	for i in range(len(jit_list[0])):
		temp_list = []
		for j in range(5):
			temp_list.append(jit_list[j][i])
		file_out.write(','.join(temp_list)+'\n')



def main():
	benchmarks = ['html5lib', 'pidigits']#['ai', 'bm_mako', 'chaos', 'django', 'rietveld']#'bm_icbd' , 'twisted_web'

	for benchmark in benchmarks:
		benchmark_file = benchmark + '_boxplot.json'
		for i in range(5):
	 		data_list = get_performance_data(benchmark_file, i)
			save_as_csv(benchmark, data_list,i)
		convert_jitted_line(benchmark)

if __name__ == '__main__':
	main()