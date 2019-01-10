library("rjson")
library("effsize")

result_root = ''
benchmarks = c('db', 'fortune', 'json', 'plaintext', 'query', 'update')
config_index = c(0,1,2,3,4)

get_data <- function(benchmark){
  config_index <- c('0','1','2','3','4')
  temp_list <- list()
  for(i in 1:5){
    print(config_index[i])
    file_in = paste(result_root, benchmark, '_', config_index[[i]], '_response_time.csv', sep = '')
    csv_data <- read.csv(file = file_in, header=FALSE, stringsAsFactors = FALSE, sep=',')
    
    temp_list[i] <- list(tail(csv_data[[1]][],600))
  }
  #print(temp_list)
  return(temp_list)
  
}


for(benchmark in 1:length(benchmarks)){
  temp_matrix <- matrix(nrow = 5*2+1, ncol = 5)
  #csv_data <- read.csv(file = paste(result_root, benchmarks[benchmark], '_performance_data.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  csv_data <- get_data(benchmarks[benchmark])
  for(i in 1:5){
    temp_vector = c()
    for(j in 1:5){
      list_A <- as.numeric(csv_data[[i]])
      list_B <- as.numeric(csv_data[[j]])
      wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
      temp_vector <- c(temp_vector, wilcox_sum$p.value)
    }
    temp_matrix[i, ]<-temp_vector
  }
  
  temp_matrix[6, ] <- c(0,0,0,0,0)
  for(i in 1:5){
    temp_vector = c()
    for(j in 1:5){
      list_A <- as.numeric(csv_data[[i]])
      list_B <- as.numeric(csv_data[[j]])
      cliff <- cliff.delta(list_A, list_B)
      temp_vector <- c(temp_vector, cliff$estimate)
    }
    temp_matrix[6+i, ]<-temp_vector
  }
  
  write.csv(temp_matrix, file=paste(result_root, 'effect_size_matrix_', benchmarks[benchmark], '.csv'))
}



