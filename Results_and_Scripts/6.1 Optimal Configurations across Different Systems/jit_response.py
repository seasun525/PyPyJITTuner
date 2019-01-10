file_in_name = 'quokka_jitted_response.csv'

ind = line.split(',')[0]
ind_list = decode_list(ind)
new_line = ','.join(map(str, ind_list))
new_line = new_line + ',' + ','.join(line.split(',')[1:])
file_out.write(new_line)
