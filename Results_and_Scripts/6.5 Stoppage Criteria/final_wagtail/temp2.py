import json
import csv
list_ind = ['011011011011011011','101101001010111000','110111011010111000','101111011101111001']
result_list = []
for ind in list_ind:
	output_path = 'tops/'+ind+'/resource_usage.csv'
	file_out = open(output_path, 'r')
	#csv_input = csv.reader(file_out, delimiter=',')
	temp_list = [[],[],[],[]]
	
	flag = True
	first_D_MEM = 0
	for row in file_out.readlines()[1:]:
		row = map(float, row.strip().split(','))
		if flag:
			first_D_MEM = row[4]
			flag = False
		temp_list[0].append(row[1])
		temp_list[1].append(row[2])
		temp_list[2].append(row[3])
		temp_list[3].append(row[4])
	result_list.append([sum(x)/len(x) for x in temp_list])


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

