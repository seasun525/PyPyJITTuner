library("rjson")
library("effsize")

individual_list <- c('div_individual_value0','div_individual_value1','div_individual_value2','div_individual_value3','div_individual_value4','div_individual_value5','div_individual_value6','div_individual_value7')

ind_num <- 8
obj_num <- 5

get_data <- function(individual, flag){
  
  benchmark_file <- paste(individual, sep='')
  con=file(benchmark_file,open="r")
  line=readLines(con)
  csv_data <- list()
  for(i in 1:length(line)){
    row <- line[[i]]
    row <- as.integer(strsplit(row, ',')[[1]])
    csv_data[[i]] <- row
  }
  close(con)
  #csv_data <- read.csv(benchmark_file, header=FALSE, stringsAsFactors = FALSE, sep=',')
  return(csv_data)
}

response_data_list <- list()
#monitor_data_list <- list()

for(i in 1:ind_num){
  response_data_list[[i]] <- get_data(individual_list[[i]], TRUE)
}

for(i in 1:obj_num){
  temp_matrix <- matrix(nrow = ind_num*2+1, ncol = ind_num)
  for(j in 1:ind_num){
    temp_vector <- c()
    for(k in 1:ind_num){
        list_A <- as.numeric(response_data_list[[j]][[i]])
        list_B <- as.numeric(response_data_list[[k]][[i]])
        wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
        #cliff <- cliff.delta(result_list[[i]][[j]], result_list[[i]][[k]])
        temp_vector <- c(temp_vector, wilcox_sum$p.value)
    }
    print(temp_vector)
    temp_matrix[j, ]<-temp_vector
  }
  temp_matrix[ind_num+1, ]<-c(0,0,0,0,0,0,0,0)
  
  for(j in 1:ind_num){
    temp_vector <- c()
    for(k in 1:ind_num){
        list_A <- as.numeric(response_data_list[[j]][[i]])
        list_B <- as.numeric(response_data_list[[k]][[i]])
        cliff <- cliff.delta(list_A, list_B)
        temp_vector <- c(temp_vector, cliff$estimate)
    }
    print(temp_vector)
    temp_matrix[j+ind_num+1, ]<-temp_vector
  }
  print(i)
  write.csv(temp_matrix, file=paste('effect_size_matrix_', i,'.csv'))
  print('+++++++++++++++++++++++++')
}

temp_matrix <- matrix(nrow = obj_num*2+1, ncol = 7)
for(i in 1:obj_num){
  temp_vector <- c()
  for(j in 2:ind_num){
    list_A <- as.numeric(response_data_list[[j-1]][[i]])
    list_B <- as.numeric(response_data_list[[j]][[i]])
    wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
    #cliff <- cliff.delta(result_list[[i]][[j]], result_list[[i]][[k]])
    temp_vector <- c(temp_vector, wilcox_sum$p.value)
  }
  print(temp_vector)
  temp_matrix[i, ]<-temp_vector
  
  temp_matrix[obj_num+1, ]<-c(0,0,0,0,0,0,0)
  
  temp_vector <- c()
  for(j in 2:ind_num){
    list_A <- as.numeric(response_data_list[[j]][[i]])
    list_B <- as.numeric(response_data_list[[j-1]][[i]])
    cliff <- cliff.delta(list_A, list_B)
    temp_vector <- c(temp_vector, cliff$estimate)
  }
  print(temp_vector)
  temp_matrix[obj_num+i+1, ]<-temp_vector
  
  
}

print(i)
write.csv(temp_matrix, file=paste('effect_size_for_slots.csv'))
print('+++++++++++++++++++++++++')

