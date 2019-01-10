library("rjson")
library("effsize")

result_root = ''
benchmarks = c('db', 'fortune', 'json', 'plaintext', 'query', 'update')
warmup_iter = c(3,4,2,2,6,10)
for(index in 1:length(benchmarks)){
  benchmark <- benchmarks[index]
  iter <- warmup_iter[index]
  response_time_list <- read.csv(file = paste(result_root, benchmark, '_2_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',') 
  print(length(response_time_list))
  list_A <- as.numeric(response_time_list[[1]][1:60*iter])
  list_B <- as.numeric(response_time_list[[1]][60*iter:7200])
  wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
  cliff <- cliff.delta(list_A, list_B)
  print(benchmark)
  print(wilcox_sum$p.value)
  print(cliff$estimate)
}
