library(ggplot2)
library(datasets)
library(grid)


result_root = ''
Ind <- 6
benchmarks_list <- c('ai', 'bm_mako', 'chaos', 'django', 'rietveld', 'html5lib', 'pidigits')
division_list <- c(600,3000,20000,4000,1600,230,4)
upper_bound <- c(0.029,0.023,0.0065,0.027,0.52,2.5,6)
warmup_iterations <- c(34,29,10,11,42,11,0)
label_upper <- c(0.0315, 0.025, 0.0070, 0.0292, 0.561, 2.65, 6.5)
warmup <- warmup_iterations[Ind]
benchmarks <- c(benchmarks_list[Ind])
div <- division_list[Ind]
upper <- upper_bound[Ind]
label_up <- label_upper[Ind]

myplot <-NA
for(index in 1:length(benchmarks)){
  #if(index != 6){
  #  next
  #}
  benchmark = benchmarks[index]
  jitted_line_matrx <- read.csv(file = paste(result_root, benchmark, '_jitted_line_R.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  jitted_line_list <- jitted_line_matrx[[3]]
  print(length(jitted_line_list))
  response_time_matrix <- read.csv(file = paste(result_root, benchmark,'_2_response_time.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')
  print(length(response_time_matrix))
  print(response_time_matrix[[1]])
  # for(i in 1:length(response_time_matrix)){
  #   for(j in 1:length(response_time_matrix[[1]])){
  #     response_time_matrix[[i]][[j]] <- response_time_matrix[[i]][[j]]
  #   }
  #   
  # }
  
  print(response_time_matrix[[1]])
  list1<-c()
  list2<-c()
  list3<-c()
  list4<-c()
  list5<-c()
  for(i in 1:50){
    #if(i == 1 | i %% 10 == 0){
    if(i < warmup){
      list4<-c(list4, c(rep(1, 30)))
    }else{
      list4<-c(list4, c(rep(2, 30)))
    }
      list1 <- c(list1, response_time_matrix[[i]])
      list2 <- c(list2, c(rep(i, 30)))
      list3 <- c(list3, c(rep(jitted_line_list[[i+1]], 30)))
      list5 <- c(list5, c(rep(mean(response_time_matrix[[i]]), 30)))
    #}
  }
  
  # for(i in 1:5){
  #   for(j in 1:10){
  #     list1 <- c(list1, response_time_matrix[[(i-1)*5+j]])
  #     list2 <- c(list2, c(rep(i, 30)))
  #     list3 <- c(list3, c(rep(jitted_line_list[[i*10]], 30)))
  #   }
  # }
  # list1 <- list1/mean(list1)

  df <- data.frame(response=list1, iteration=list2, jitline=list3, group=list4, avg=list5)
  windowsFonts(TimesNew=windowsFont("Times New Roman"))
  text_jitting <- textGrob("jitting", gp=gpar(fontfamily ="serif", fontsize=20))
  text_jitted <- textGrob("jitted", gp=gpar(fontfamily="serif",fontsize=20))
  block1 <- textGrob("|<------", gp=gpar(fontsize=20))#, fontface="bold"))
  block2 <- textGrob("------>|<------------------------------------", gp=gpar(fontsize=20))#, fontface="bold"))
  block3 <- textGrob("------------------------------------>|", gp=gpar(fontsize=20))#, fontface="bold"))
  myplot <- ggplot(df) +
    #geom_rect(aes(xmin = -Inf, xmax = warmup, ymin = -Inf, ymax = Inf), fill = "pink", alpha = 0.05) +
    geom_line(aes(x=iteration, y = (jitline-450)/90*1.5+1.0, size = 0.3)) +
    scale_size(range=c(0.1, 1), guide=FALSE) +
    #scale_size_manual(values = c(10,10)) +
    #geom_line(aes(x=iteration, y = (jitline-450)/100*1.5+1.0)) +
    #geom_line(aes(x=iteration, y = (jitline-450)/100+1.5)) +
    #geom_line(aes(x=iteration, y = avg),color="red") +
    geom_boxplot(aes(x=factor(iteration), y=response)) +
    scale_y_continuous(limits = c(1, upper), sec.axis = sec_axis(~(.-1)*90/1.5+450, name = "Number of jitted lines")) +
    scale_x_discrete(breaks = seq(0, 50, 5)) +
    ylab("Response time (second)") +
    xlab("Number of iterations")+
    geom_vline(xintercept = warmup, color = "red", linetype = "dashed") +
    #annotate("text", label = "Mean = 5", x = 20, y = 0.029, color = "black") +
    #facet_grid(.~group,scales='free',space='free_x',as.table=FALSE)+
    
    annotation_custom(block1,xmin=2.4,xmax=2.4,ymin=label_up,ymax=label_up) +
    annotation_custom(text_jitting,xmin=warmup/2,xmax=warmup/2,ymin=label_up,ymax=label_up) +
    annotation_custom(block2,xmin=warmup+5.68,xmax=warmup+5.68,ymin=label_up,ymax=label_up) + #0.73
    annotation_custom(text_jitted,xmin=(warmup+50)/2,xmax=(warmup+50)/2,ymin=label_up,ymax=label_up) +
    annotation_custom(block3,xmin=42.8,xmax=42.8,ymin=label_up,ymax=label_up) +
    theme(plot.margin = unit(c(2,1,1,1), "lines"), text = element_text(family="serif", size=20))

  #change the font of jitting and jitted to be same as x-axis.

  gt <- ggplot_gtable(ggplot_build(myplot))
  gt$layout$clip[gt$layout$name == "panel"] <- "off"
  myplot<-grid.draw(gt)
  pdf(paste(result_root, benchmark, '_boxplot.pdf', sep=''))
  print(myplot)
  dev.off()
  #print(myplot)
  
  #print(paste(result_root, benchmark, '_beanplot.pdf', sep=''))

  # pdf(paste(result_root, benchmark, '_boxplot3.pdf', sep=''))
  # print(myplot)
  # dev.off()
  # print(myplot)
}

#default
# block1 <- textGrob("|<--", gp=gpar(fontsize=13, fontface="bold"))
# block2 <- textGrob("-->|<--", gp=gpar(fontsize=13, fontface="bold"))
# block3 <- textGrob("-->|", gp=gpar(fontsize=13, fontface="bold"))
# myplot <- ggplot(df) + 
#   #geom_rect(aes(xmin = -Inf, xmax = warmup, ymin = -Inf, ymax = Inf), fill = "pink", alpha = 0.05) +
#   geom_line(aes(x=iteration, y = jitline/div)) +
#   geom_line(aes(x=iteration, y = avg),color="red") +
#   geom_boxplot(aes(x=factor(iteration), y=response)) +
#   scale_y_continuous(limits = c(0, upper), sec.axis = sec_axis(~.*div, name = "number of jitted line ")) +
#   scale_x_discrete(breaks = seq(0, 50, 5)) +
#   ylab("response time (second)") +
#   xlab("number of iterations")+
#   geom_vline(xintercept = warmup, color = "red", linetype = "dashed") +
#   #annotate("text", label = "Mean = 5", x = 20, y = 0.029, color = "black") + 
#   #facet_grid(.~group,scales='free',space='free_x',as.table=FALSE)+
#   theme(plot.margin = unit(c(2,1,1,1), "lines"), text = element_text(size=20))+
#   annotation_custom(block1,xmin=2,xmax=2,ymin=label_up,ymax=label_up) + 
#   annotation_custom(text_jitting,xmin=warmup/2,xmax=warmup/2,ymin=label_up,ymax=label_up) + 
#   annotation_custom(block2,xmin=warmup,xmax=warmup,ymin=label_up,ymax=label_up) + #0.73
#   annotation_custom(text_jitted,xmin=(warmup+50)/2,xmax=(warmup+50)/2,ymin=label_up,ymax=label_up) +
#   annotation_custom(block3,xmin=49,xmax=49,ymin=label_up,ymax=label_up)

#7
# block1 <- textGrob("|<--", gp=gpar(fontsize=13, fontface="bold"))
# block2 <- textGrob("-->|<--", gp=gpar(fontsize=13, fontface="bold"))
# block3 <- textGrob("-->|", gp=gpar(fontsize=13, fontface="bold"))
# myplot <- ggplot(df) + 
#   #geom_rect(aes(xmin = -Inf, xmax = warmup, ymin = -Inf, ymax = Inf), fill = "pink", alpha = 0.05) +
#   geom_line(aes(x=iteration, y = jitline/div)) +
#   geom_line(aes(x=iteration, y = avg),color="red") +
#   geom_boxplot(aes(x=factor(iteration), y=response)) +
#   scale_y_continuous(limits = c(0, upper), sec.axis = sec_axis(~.*div, name = "number of jitted line ")) +
#   scale_x_discrete(breaks = seq(0, 50, 5)) +
#   ylab("response time (second)") +
#   xlab("number of iterations")+
#   geom_vline(xintercept = 1, color = "red", linetype = "dashed") +
#   #annotate("text", label = "Mean = 5", x = 20, y = 0.029, color = "black") + 
#   #facet_grid(.~group,scales='free',space='free_x',as.table=FALSE)+
#   theme(plot.margin = unit(c(2,1,1,1), "lines"), text = element_text(size=20))+
#   annotation_custom(block1,xmin=2,xmax=2,ymin=label_up,ymax=label_up) + 
#   #annotation_custom(text_jitting,xmin=warmup/2,xmax=warmup/2,ymin=label_up,ymax=label_up) + 
#   #annotation_custom(block2,xmin=warmup,xmax=warmup,ymin=label_up,ymax=label_up) + #0.73
#   annotation_custom(text_jitted,xmin=(warmup+50)/2,xmax=(warmup+50)/2,ymin=label_up,ymax=label_up) +
#   annotation_custom(block3,xmin=49,xmax=49,ymin=label_up,ymax=label_up)

