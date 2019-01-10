import json
import csv
list_ind = ['011011011011011011','010101100100111001','111010010000111011','111110000000110100']
result_list = []
for ind in list_ind:
	output_path = 'tops/'+ind+'/individual_value'
	file_out = open(output_path, 'r')
	csv_input = csv.reader(file_out, delimiter=',')
	temp_list = []
	for row in csv_input:
		row = map(float, row)
		temp_list.append(sum(row)/len(row))
	result_list.append(temp_list)

for i in range(len(list_ind)):
	temp_list = []
	for j in range(3):
		temp_list.append(float(result_list[0][j]-result_list[i][j])/result_list[0][j])
	result_list.append(temp_list)

output_path = 'statistical_analysis/average.csv'
csv_output = open(output_path, 'w')
csv_output.write('obj_1,obj_2,obj_3\n')
for row in result_list[:len(list_ind)]:
	csv_output.write(','.join(map(str, row))+'\n')

csv_output.write('\n')

for row in result_list[len(list_ind):]:
	csv_output.write(','.join(map(str, row))+'\n')




