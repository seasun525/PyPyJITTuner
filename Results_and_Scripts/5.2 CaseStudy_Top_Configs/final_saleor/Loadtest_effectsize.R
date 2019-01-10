library("rjson")
library("effsize")

individual_list <- c('011011011011011011','110111001000111011','110110101001101000','110111110001101011')

ind_num <- 4

get_data <- function(individual, flag){
  
  benchmark_file <- paste('tops/',individual,'/individual_value', sep='')
  con=file(benchmark_file,open="r")
  line=readLines(con)
  csv_data <- list()
  for(i in 1:length(line)){
    row <- line[[i]]
    row <- as.integer(strsplit(row, ',')[[1]])
    csv_data[[i]] <- row
  }
  close(con)
  return(csv_data)
}

response_data_list <- list()

for(i in 1:ind_num){
  response_data_list[[i]] <- get_data(individual_list[[i]], TRUE)
  print( response_data_list[[i]])
}

temp_matrix <- matrix(nrow = (ind_num-1)*2+1, ncol = 13)
for(i in 2:ind_num){
  temp_vector <- c()
  for(j in 1:13){
    list_A <- as.numeric(response_data_list[[1]][[j]])
    list_B <- as.numeric(response_data_list[[i]][[j]])
    wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
    #cliff <- cliff.delta(result_list[[i]][[j]], result_list[[i]][[k]])
    temp_vector <- c(temp_vector, wilcox_sum$p.value)
  }
  print(temp_vector)
  temp_matrix[i-1, ]<-temp_vector
}
temp_matrix[ind_num, ]<-c(0,0,0,0,0,0,0,0,0,0,0,0,0)

for(i in 2:ind_num){
  temp_vector <- c()
  for(j in 1:13){
    
    list_A <- as.numeric(response_data_list[[1]][[j]])
    list_B <- as.numeric(response_data_list[[i]][[j]])
    cliff <- cliff.delta(list_A, list_B)
    temp_vector <- c(temp_vector, cliff$estimate)
  
  }
  print(temp_vector)
  temp_matrix[i+ind_num-1, ]<-temp_vector
  
}

write.csv(temp_matrix, file=paste('statistical_analysis/', 'validate.csv'))

