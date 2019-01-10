def decode_list(individual):
    temp_list = []
    for i in range(6):
        string_value = ''.join(map(str, individual[i*3:(i+1)*3]))
        value = int(string_value, 2)
        temp_list.append(value)

    return temp_list

file_in_name = 'Quokka\quokka_jitted_response.csv'
file_out_name = 'Quokka\quokka_jitted_response_decoded.csv'
file_in = open(file_in_name, 'r')
file_out = open(file_out_name, 'w')

for  line in file_in.readlines():
	ind = line.split(',')[0]
	ind_list = decode_list(ind)
	new_line = ','.join(map(str, ind_list))
	new_line = new_line + ',' + ','.join(line.split(',')[1:])
	file_out.write(new_line)

file_out.close()
