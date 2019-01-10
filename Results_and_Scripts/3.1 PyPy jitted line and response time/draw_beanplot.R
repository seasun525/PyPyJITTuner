library(ggplot2)
library(beanplot)

result_root = ''
Ind <- 6
benchmarks_list <- c('ai', 'bm_mako', 'chaos', 'django', 'rietveld', 'html5lib', 'pidigits')
division_list <- c(600,3000,20000,4000,1600,250,4)
upper_bound <- c(0.029,0.023,0.0065,0.027,0.52,2.5,6)
warmup_iterations <- c(34,29,10,11,42,11,0)

warmup <- warmup_iterations[Ind]
benchmarks <- c(benchmarks_list[Ind])
div <- division_list[Ind]
upper <- upper_bound[Ind]

print(benchmarks)
myplot <-NA
for(index in 1:length(benchmarks)){
  benchmark = benchmarks[index]
  jitted_line_matrx <- read.csv(file = paste(result_root, benchmark, '_jitted_line_R.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  jitted_line_list <- jitted_line_matrx[[3]]
  print(length(jitted_line_list))
  response_time_matrix <- read.csv(file = paste(result_root, benchmark,'_2_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  print(length(response_time_matrix))
  print(response_time_matrix[[1]])
  
  for(i in 1:length(response_time_matrix)){
    for(j in 1:length(response_time_matrix[[1]])){
      response_time_matrix[[i]][[j]] <- response_time_matrix[[i]][[j]]
    }
    
  }
  
  print(response_time_matrix[[1]])
  list1<-c()
  list2<-c()
  list3<-c()
  warming_list <- c()
  warmed_list <- c()
  index <- c()
  index2 <- c()
  
  # index <- c(0)
  # index2 <- c('A')
  # warming_list <- (response_time_matrix[[1]][[1]])
  # list1 <- c(response_time_matrix[[1]][[1]])
  # list2 <- c(1)
  # list3 <- c(1)
  for(i in 1:50){
    if(i <= warmup){
      index <- c(index, rep(1, 30))
      index2 <- c(index2, rep('A', 30))
      warming_list<-c(warming_list, response_time_matrix[[i]])
    }else{
      index <- c(index, rep(1, 30))
      index2 <- c(index2, rep('B', 30))
      #warming_list<-c(warming_list, response_time_matrix[[i]])
      warmed_list <-c(warmed_list, response_time_matrix[[i]])
    }
    list1 <- c(list1, response_time_matrix[[i]])
    list2 <- c(list2, c(rep(i, 30)))
    list3 <- c(list3, c(rep(jitted_line_list[[i+1]], 30)))

  }
  
  #df <- data.frame(response=list1, iteration=list2, y=list3, ind=index, ind2=index2, warm=warming_list)
  #df <- data.frame(response=list1, iteration=list2, jitline=list3, ind=index, warm=warming_list)
  #myplot<-ggplot(df, aes(x=ind, y=warm))+geom_boxplot()+geom_violin(fill='lightblue', alpha=0.5)+geom_jitter(position = position_jitter(width = .1))
  #myplot <- beanplot(df$warm~df$ind*df$ind2, ylim= c(0,1.5))
  # myplot <- beanplot(df, x=index, y=warming_list, side='both', border='NA', 
  #                    col=list('gray',c('red','white')),
  # #                    ylab='Wind Speed (m/s)' ,what=c(1,1,1,0),xaxt ='n')
  # myplot <- beanplot(df$warm~df$ind*df$ind2, ll = 0.04,
  #                    main = paste("benchmark ",benchmark), side = "both", xlab="jitting |  jitted",
  #                    col = list("black", c("gray", "black")),
  #                    ylim = c(min(df$warm),max(df$warm)), log="y")#axes=F)
  # 
  print(max(warming_list))
  print(max(warmed_list))
  myplot <- beanplot(warming_list, warmed_list, log="", 
                     ylab="Response Time (sec)", xlab="   warm-up | warmed up", side="both", border=NA, 
                     what = c(FALSE, TRUE, TRUE, FALSE), col=list("black", "grey"), 
                     overallline = "mean",
                     names=c("Test A", "Test B"), show.names=FALSE, cex.lab=1.5, 
                     cex.main=2,beanlinewd=1)

  legend("topright", fill = c("black", "gray"),legend = c("warm-up", "warmed up"))
  print(myplot)
  
  
  # pdf(paste(result_root, benchmark, '_beanplot.pdf', sep=''))
  # print(myplot)
  # dev.off()
  # print(myplot)

}
print()
print(sort(table(round(warming_list, 2)))[-1])
print(sort(table(round(warmed_list, 2)))[-1])
