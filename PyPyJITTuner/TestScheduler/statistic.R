library("effsize")
args <- commandArgs(TRUE)
options(warn=-1)
measure_cllif <- function(input1, input2){
  input1_list <- as.numeric(strsplit(input1, ',')[[1]])
  input2_list <- as.numeric(strsplit(input2, ',')[[1]])
  result_list = cllif_delta(input1_list, input2_list)

  wilcox_sum <- wilcox.test(input1_list, input2_list, paired=FALSE)
  
  print(paste(result_list, wilcox_sum$p.value, sep = ','))
}

cllif_delta <- function(input1, input2){

  #list_1 <- as.numeric(result_data_1[[1]])
  #list_2 <- as.numeric(result_data_2[[1]])
  
  cliff <- cliff.delta(input1, input2)
  return(cliff$estimate)
}

input1 <- args[1]
input2 <- args[2]
measure_cllif(input1, input2)


