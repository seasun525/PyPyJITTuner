library("rjson")
library("effsize")

result_root = ''
benchmarks = c('db', 'fortune', 'json')#, 'pidigits'
config_index = c(1,2,4,5,6,7,8,9,10,11)


temp_matrix <- matrix(nrow = length(benchmarks)*2+1, ncol = length(config_index))
for(benchmark in 1:length(benchmarks)){
  temp_vector = c()
  for(j in 1:length(config_index)){
    csv_data1 <- NA
    csv_data2 <- NA
    csv_data1 <- read.csv(file = paste(result_root, benchmarks[benchmark],'_' ,config_index[j]-1, '_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
    csv_data2 <- read.csv(file = paste(result_root, benchmarks[benchmark],'_' ,2, '_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')

    list_A <- as.numeric(csv_data1[[1]])
    list_B <- as.numeric(csv_data2[[1]])
    wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
    temp_vector <- c(temp_vector, wilcox_sum$p.value)
  }
  temp_matrix[benchmark, ]<-temp_vector
}

temp_matrix[length(benchmarks)+1, ] <- c(0,0,0,0,0,0,0,0,0,0)

for(benchmark in 1:length(benchmarks)){
  temp_vector = c()
  for(j in 1:length(config_index)){
    csv_data1 <- read.csv(file = paste(result_root, benchmarks[benchmark],'_' ,config_index[j]-1, '_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
    csv_data2 <- read.csv(file = paste(result_root, benchmarks[benchmark],'_' ,2, '_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')

    list_A <- as.numeric(csv_data1[[1]])
    list_B <- as.numeric(csv_data2[[1]])
    cliff <- cliff.delta(list_A, list_B)
    temp_vector <- c(temp_vector, cliff$estimate)
  }
  temp_matrix[length(benchmarks)+1+benchmark, ]<-temp_vector

}

write.csv(temp_matrix, file=paste(result_root, 'pypy_effectsize_compare_to_default.csv'))
