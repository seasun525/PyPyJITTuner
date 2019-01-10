import json
import csv
list_ind = ['011011011011011011','010101100100111001','111010010000111011','111110000000110100']
string_list = ['mongo_statistic_CPU.csv', 'mongo_statistic_Memory.csv', 'worker_statistic_CPU.csv', 'worker_statistic_Memory.csv']

def get_list(ind, name):
	output_path = 'tops/'+ind+'/'+name
	file_in = open(output_path, 'r')
	temp_list = []
	for line in file_in.readlines():
		temp_list.append(float(line.strip()))
	return temp_list


result_list = []
for ind in list_ind:

	temp_list = []
	for name in string_list:
		row = get_list(ind, name)
		temp_list.append(sum(row)/len(row))
	result_list.append(temp_list)

for i in range(len(list_ind)):
 	temp_list = []
	for j in range(4):
		temp_list.append(float(result_list[0][j]-result_list[i][j])/result_list[0][j])
	result_list.append(temp_list)


output_path = 'statistical_analysis/average2.csv'
csv_output = open(output_path, 'w')
csv_output.write('obj_1,obj_2,obj_3,obj_4\n')
for row in result_list[:len(list_ind)]:
	csv_output.write(','.join(map(str, row))+'\n')

csv_output.write('\n')

for row in result_list[len(list_ind):]:
	csv_output.write(','.join(map(str, row))+'\n')


