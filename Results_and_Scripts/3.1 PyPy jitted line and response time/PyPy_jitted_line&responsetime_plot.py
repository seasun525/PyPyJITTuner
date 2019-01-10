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
	for row in open(benchmark+'_jitted_line.csv', 'r').readlines():
		jitted_line.append(map(int,row.split(',')))

	response_time_list = ast.literal_eval(open(benchmark+'_boxplot.json', 'r').readline().split('\"')[1])#json.load(open(benchmark+'_boxplot.json', 'r').readline())
	print len(response_time_list)
	print len(response_time_list[0])
	print len(response_time_list[0][0])
	print len(response_time_list[0][0][0])
	#bprint len(response_time_list[1][1][1])
	x = []
	y = []
	boxplot_trace_list = []
	response_time_list2 = []
	for i in range(len(jitted_line[0][1:])):
		x = x+[i+1]*30
		temp_list = []
		for j in range(30):
			temp_list.append(response_time_list[2][0][j][i])
		response_time_list2.append(temp_list)
		y = y + temp_list

	trace_list = []
	temp_trace = go.Scatter(
			x = range(51),
			y = jitted_line[2],
			mode = 'lines',
			yaxis='y2',
			#line = dict(color = color_list[i]),
			name = 'jitted_line'
		)
	trace_list.append(temp_trace)
	temp_trace = go.Box(
			y = y,
			x = x,
			name = 'execution time',
			boxpoints = False)
	trace_list.append(temp_trace)

	layout = go.Layout(
		title=benchmark,
		yaxis=dict(
			title='execution time (second)',
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
	        range=[0,max(jitted_line[2])*1.5]
    	),
    	xaxis=dict(
    		title='number of iterations'
    		),
		boxmode='group'
	)

	fig = go.Figure(data=trace_list, layout=layout)
	plot(fig,filename=benchmark+'_plot.html')
	py.image.save_as(fig, filename=benchmark+'_plot.png')

def main():
	benchmarks = ['ai']#['ai','bm_mako', 'chaos', 'django', 'rietveld', 'html5lib', 'pidigits']#
	for benchmark in benchmarks:
		draw_for_benchmark(benchmark)


if __name__ == '__main__':
	main()