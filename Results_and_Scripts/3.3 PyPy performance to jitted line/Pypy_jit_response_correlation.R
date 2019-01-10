
result_root = ''
benchmarks = c('ai', 'bm_mako', 'chaos', 'django', 'rietveld', 'html5lib', 'pidigits')
config_index_list <- c('0', '1', '2', '3', '4')
get_data <- function(benchmark, index){
  input_file <- paste(result_root,benchmark,'_response_time_R.csv', sep='')
  response_time_list <- read.csv(file=input_file,head=FALSE,sep=",")
  res <- response_time_list[[index]]
  
  input_file <- paste(result_root,benchmark,'_jitted_line_R.csv', sep='')
  jitted_line_list <- read.csv(file=input_file,head=FALSE,sep=",")
  jit <- jitted_line_list[[index]][2:51]

  return(list(jit=jit, res=res))
}

for(index in 1:length(benchmarks)){
  benchmark <- benchmarks[[index]]
  for(j in 1:5){
    config_index <- config_index_list[j]
    result_list <- get_data(benchmark, j)
    jitted_line_list <- result_list$jit
    response_time_list <- result_list$res
    print(benchmark)
    print(config_index)
    result = cor.test(x=jitted_line_list,y=response_time_list,method = 'spearman', exact=TRUE)
    print(result)
  }
}
