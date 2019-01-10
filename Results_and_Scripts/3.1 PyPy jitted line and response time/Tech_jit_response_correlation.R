
result_root = ''
benchmarks = c('db', 'fortune', 'json', 'plaintext', 'query', 'update')
config_index_list <- c('0', '1', '2', '3', '4')
get_data <- function(benchmark, index){
  input_file <- paste(result_root,benchmark,'_',index,'_response_time.csv', sep='')
  response_time_list <- read.csv(file=input_file,head=FALSE,sep=",")
  temp_vector <- c()
  temp <- 0
  for(i in 1:length(response_time_list[[1]])){
    temp = temp+response_time_list[[1]][[i]]
    if(i %% 60 == 0){
      temp <- temp/60
      temp_vector <- c(temp_vector, temp)
      temp <- 0
    }
  }
  #print(temp_vector)
  jitted_line_file <- paste(result_root,benchmark,'_',index,'_jitted_lines_over_time.csv', sep='')
  con=file(jitted_line_file,open="r")
  line=readLines(con)
  jitted_lines <- list()
  for(i in 1:length(line)){
    row <- line[[i]]
    row <- as.integer(strsplit(row, ',')[[1]])
    jitted_lines[[i]] <- row
  }
  close(con)
  #csv_data <- read.csv(benchmark_file, header=FALSE, stringsAsFactors = FALSE, sep=',')
  return(list(jit=jitted_lines, res=temp_vector))
}

for(index in 1:length(benchmarks)){
  benchmark <- benchmarks[[index]]
  for(j in 1:5){
    config_index <- config_index_list[j]
    result_list <- get_data(benchmark, config_index)
    jitted_line_list <- result_list$jit
    response_time_list <- result_list$res
    print(benchmark)
    print(config_index)
    result = cor(x=jitted_line_list[[1]],y=response_time_list,method = 'spearman')
    print(result)
  }
}
