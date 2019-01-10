library(ggplot2)
library(datasets)

result_root = ''
benchmarks_list = c('db', 'fortune', 'json', 'plaintext', 'query', 'update')
Ind <- 2
division_list <- c(15, 15, 15, 0.5, 0.8, 0.25 )
upper_bound <- c(170, 160, 90, 3000, 3000, 9000)
benchmarks <- c(benchmarks_list[Ind])
div<- division_list[Ind]
upper <- upper_bound[Ind]
interval<- 1 #minute
myplot <-NA
for(index in 1:length(benchmarks)){
  benchmark <- benchmarks[index]
  jitted_line_file <- paste(result_root,benchmark,'_2_jitted_lines_over_time.csv', sep='')
  con=file(jitted_line_file,open="r")
  line=readLines(con)
  jitted_lines <- list()
  for(i in 1:length(line)){
    row <- line[[i]]
    row <- as.integer(strsplit(row, ',')[[1]])
    jitted_lines[[i]] <- row
  }
  close(con)
  jitted_line_list <- jitted_lines[[1]]
  
  response_time_matrix <- read.csv(file = paste(result_root, benchmark,'_2_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  print(length(response_time_matrix))
  print(length(response_time_matrix[[1]]))
  print(length(jitted_line_list))
  list1<-c()
  list2<-c()
  list3<-c()
  list1 <- c(list1, response_time_matrix[[i]])
  list1 <- list1/1000
  for(i in 1:(30/interval)){
    
    list2 <- c(list2, c(rep(i, 60*interval)))
    temp <- (i-1)*interval+1
    list3 <- c(list3, c(rep(jitted_line_list[[temp]], 60*interval)))
  }
  
  df <- data.frame(response=list1, iteration=list2, jitline=list3)
  
  myplot <- ggplot(df, aes(x=factor(iteration), y=response)) +
    geom_boxplot() +
    geom_line(aes(x=iteration, y = jitline/div)) +
    scale_y_continuous(limits = c(0, upper), sec.axis = sec_axis(~.*div, name = "number of jitted line")) +
    scale_x_discrete(breaks = seq(0, 120, 10)) +
    ylab("response time (Millisecond)") +
    xlab("execution time (Minute)") +
    theme(text = element_text(size=20))
    
  pdf(paste(result_root, benchmark, '_boxplot3.pdf', sep=''))
  print(myplot)
  dev.off()
  print(myplot)
}
