import json
import csv
import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go 
import sys
from plotly import tools

page_index = [[1,2,3,4,5], #add blog
            [6,7,8,9,10], #edit blog
            [11,12,13,14]]
#default_value = [56,34,269,144,74,89,189,243,177,333,89,91,11.7318888889,11.7318888889]
#page_list = ['add_blog', 'add_event', 'edit_blog', 'view_blog', 'view_event']
#color_list = ['#FE642E', '#F7FE2E', '#64FE2E', '#2EFEC8', '#2E64FE', '#CC2EFA', '#FE2E9A', '#A4A4A4', '#1C1C1C']
interval = 60 #second
duration = 200 #minute

def load_value_matrix(json_data):
	value_matrix = json_data['values']
	result = []
	for i in range(len(value_matrix[0])):
		temp_list = []
		for j in range(len(value_matrix)):
			temp_list.append(value_matrix[j][i])
		result.append(temp_list)

	return result

def main():
	gen_matrix = []
	
	file_input = open("jmeter_responses.csv", 'r')
	lines = file_input.readlines()
	#gen_matrix.append(load_value_matrix(json_data))
	start_time = int(lines[1].split(',')[0])/1000
	result = []
	for scenario in range(len(page_index)):
		temp_list = []
		result_list = []
		count = 0
		print len(lines)
		for line in lines[1:]:
			label = int(line.split(',')[2].split(' ')[0])
			if label in page_index[scenario]:
				timestamp = int(line.split(',')[0])/1000
				elapsed = int(line.split(',')[1])
				if (timestamp - start_time) / 60 == count:
					temp_list.append(elapsed)
				else:
					if (timestamp - start_time) / 60 > count:

						result_list.append(float(sum(temp_list))/len(temp_list))
						temp_list = []
						count += 1
		result.append(result_list)

	trace_list = []

	for i in range(len(page_index)):
		trace0 = go.Scatter(
			x = range(len(result[i])),
			y = result[i],
			mode = 'lines',
			#line = dict(color = color_list[i]),
			name = str(i)
		)
		trace_list.append(trace0)

	layout = dict(title = 'Response time over time',
		xaxis = dict(title = 'Minute'),
		yaxis = dict(title = 'average response time for requests in a scenario (MSec)'),
		)

	fig = dict(data=trace_list, layout=layout)
	plot(fig, filename='response_time_over_time.html')


if __name__ == '__main__':
	main()



