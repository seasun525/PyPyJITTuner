library("rjson")
library("effsize")
ind_num <- 4

individual_list <- c('011011011011011011','110111001000111011','110110101001101000','110111110001101011')
string_list <- c('postgres_statistic_CPU.csv', 'postgres_statistic_Memory.csv', 'worker_statistic_CPU.csv', 'worker_statistic_Memory.csv')
string_list2 <- c('13_postgres_CPU', '14_postgres_Memory', '15_worker_CPU', '16_worker_Memory')
get_data <- function(individual, flag){

  benchmark_file <- paste('tops/',individual,'/', 'resource_usage.csv', sep='')

  csv_data <- read.csv(file=benchmark_file,head=TRUE,sep=",")

  return(csv_data) 
}

response_data_list <- list()
monitor_data_list <- list()

for(i in 1:4){
  temp_list <- list()
  for(j in 1:4){
    #response_data_list[[i]] <- get_data(individual_list[[i]], TRUE)
    temp_list[[j]] <- get_data(individual_list[[i]], string_list[[j]])[[1+j]]
    print(temp_list[[j]])
  }
  response_data_list[[i]] <- temp_list
}

print(response_data_list[[i]])

for(i in 1:4){
  temp_matrix <- matrix(nrow = 9, ncol = 4)
  for(j in 1:4){
    temp_vector <- c()
    for(k in 1:4){
      
        list_A <- as.numeric(response_data_list[[j]][[i]])
        list_B <- as.numeric(response_data_list[[k]][[i]])
        wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
        #cliff <- cliff.delta(result_list[[i]][[j]], result_list[[i]][[k]])
        temp_vector <- c(temp_vector, wilcox_sum$p.value)
    }
    print(temp_vector)
    temp_matrix[j, ]<-temp_vector
  }
  temp_matrix[5, ]<-c(0,0,0,0)
  
  for(j in 1:4){
    temp_vector <- c()
    for(k in 1:4){

        list_A <- as.numeric(response_data_list[[j]][[i]])
        list_B <- as.numeric(response_data_list[[k]][[i]])
        cliff <- cliff.delta(list_A, list_B)
        temp_vector <- c(temp_vector, cliff$estimate)
    }
    print(temp_vector)
    temp_matrix[j+5, ]<-temp_vector
  }
  print(i)
  write.csv(temp_matrix, file=paste('statistical_analysis/', 'effect_size_matrix_', string_list2[i],'.csv'))
  print('+++++++++++++++++++++++++')
}

ind_num<-4
obj_num<-4
temp_matrix <- matrix(nrow = ind_num*2+1, ncol = obj_num)
for(i in 1:ind_num){
  temp_vector <- c()
  for(j in 1:obj_num){
    list_A <- as.numeric(response_data_list[[1]][[j]])
    list_B <- as.numeric(response_data_list[[i]][[j]])
    wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
    #cliff <- cliff.delta(result_list[[i]][[j]], result_list[[i]][[k]])
    temp_vector <- c(temp_vector, wilcox_sum$p.value)
  }
  print(temp_vector)
  temp_matrix[i, ]<-temp_vector
  
  temp_matrix[ind_num+1, ]<-c(0,0,0,0)
  
  temp_vector <- c()
  for(j in 1:obj_num){
    list_A <- as.numeric(response_data_list[[1]][[j]])
    list_B <- as.numeric(response_data_list[[i]][[j]])
    cliff <- cliff.delta(list_A, list_B)
    temp_vector <- c(temp_vector, cliff$estimate)
  }
  print(temp_vector)
  temp_matrix[ind_num+i+1, ]<-temp_vector
  
}

print(i)
write.csv(temp_matrix, file=paste('statistical_analysis/', 'effect_size_for_slots2.csv'))
print('+++++++++++++++++++++++++')
