import json
import csv
import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go 
import sys
from plotly import tools
import ast

num_of_run = 30

py.sign_in('seasun', 'h9t1XIkrqAnwC8A8Y00u')

def draw_for_benchmark(benchmark):
	jitted_line = []
	for row in open(benchmark+'_2_jitted_lines_over_time.csv', 'r').readlines():
		jitted_line.extend(map(int,row.split(',')))
	response_time_list = []
	for row in open(benchmark+'_2_response_time.csv', 'r').readlines():
		response_time_list.append(int(row.strip())/1000)
	
	print len(response_time_list)
	print len(jitted_line)

	x = []
	y = response_time_list
	for i in range(24):
		x = x+[i*5]*300
		
	print len(x)
	trace_list = []
	temp_trace = go.Scatter(
			x = range(120),
			y = jitted_line,
			mode = 'lines',
			yaxis='y2',
			#line = dict(color = color_list[i]),
			name = 'jitted_line'
		)
	trace_list.append(temp_trace)
	temp_trace = go.Box(
			y = y,
			x = x,
			name = 1,
			boxpoints = False)
	trace_list.append(temp_trace)

	layout = go.Layout(
		title=benchmark,
		yaxis=dict(
			title='execution time (Msec)',
			zeroline=False,
			range=[0,max(y)*1.5]
		),
		yaxis2=dict(
	        title='number of lines',
	        titlefont=dict(
	            color='rgb(148, 103, 189)'
	        ),
	        tickfont=dict(
	            color='rgb(148, 103, 189)'
	        ),
	        overlaying='y',
	        side='right',
	        range=[0,max(jitted_line)*1.5]
    	),
    	xaxis=dict(
    		title='time in mins'
    		),
		boxmode='group'
	)

	fig = go.Figure(data=trace_list, layout=layout)
	plot(fig,filename=benchmark+'_plot.html')
	py.image.save_as(fig, filename=benchmark+'_plot.png')

def main():
	benchmarks = ['db', 'fortune', 'json', 'plaintext', 'query', 'update']
	for benchmark in benchmarks:
		draw_for_benchmark(benchmark)


if __name__ == '__main__':
	main()