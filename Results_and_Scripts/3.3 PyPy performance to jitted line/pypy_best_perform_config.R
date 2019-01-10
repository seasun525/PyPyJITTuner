library("rjson")
library("effsize")

result_root = ''
benchmarks = c('ai', 'bm_mako', 'chaos', 'django', 'html5lib', 'pidigits', 'rietveld')
config_index = c(0,1,2,3,4)


for(benchmark in 1:length(benchmarks)){
  temp_matrix <- matrix(nrow = 5*2+1, ncol = 5)
  #csv_data <- read.csv(file = paste(result_root, benchmarks[benchmark], '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  
  for(i in 1:5){
    temp_vector = c()
    for(j in 1:5){
      csv_data1 <- read.csv(file = paste(result_root, benchmarks[benchmark], '_', i-1, '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
      csv_data2 <- read.csv(file = paste(result_root, benchmarks[benchmark], '_', j-1, '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
      
      list_A <- as.numeric(csv_data1[[1]])
      list_B <- as.numeric(csv_data2[[1]])
      wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
      temp_vector <- c(temp_vector, wilcox_sum$p.value)
    }
    temp_matrix[i, ]<-temp_vector
  }
  
  temp_matrix[6, ] <- c(0,0,0,0,0)
  for(i in 1:5){
    temp_vector = c()
    for(j in 1:5){
      csv_data1 <- read.csv(file = paste(result_root, benchmarks[benchmark], '_', i-1, '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
      csv_data2 <- read.csv(file = paste(result_root, benchmarks[benchmark], '_', j-1, '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')

      list_A <- as.numeric(csv_data1[[1]])
      list_B <- as.numeric(csv_data2[[1]])
      cliff <- cliff.delta(list_A, list_B)
      temp_vector <- c(temp_vector, cliff$estimate)
    }
    temp_matrix[6+i, ]<-temp_vector
  }
  
  write.csv(temp_matrix, file=paste(result_root, 'effect_size_matrix_', benchmarks[benchmark], '.csv'))
}

csv_data1 <- read.csv(file = paste(result_root, 'ai', '_', 4, '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
csv_data2 <- read.csv(file = paste(result_root, 'ai', '_', 1, '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')

list_A <- as.numeric(csv_data1[[1]])
list_B <- as.numeric(csv_data2[[1]])
cliff <- cliff.delta(list_A, list_B)
temp_vector <- c(temp_vector, cliff$estimate)
print(cliff$estimate)
print(mean(list_A))
print(mean(list_B))

