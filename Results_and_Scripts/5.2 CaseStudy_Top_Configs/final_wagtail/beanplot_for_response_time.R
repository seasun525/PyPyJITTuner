library(ggplot2)
library(beanplot)
windowsFonts(TimesNew=windowsFont("Times New Roman"))
result_root = ''

individual_list <- c('011011011011011011','101101001010111000','110111011010111000','101111011101111001')
objective_list <- c('Create Blog', 'Create Event', 'Edit Blog', 'View Blog', 'View Event')
config_list <- c('default', 'top1', 'top2', 'top3')
ind_num <- 4
obj_num <- 5

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
  #csv_data <- read.csv(benchmark_file, header=FALSE, stringsAsFactors = FALSE, sep=',')
  return(csv_data)
}

response_data_list <- list()
#monitor_data_list <- list()

for(i in 1:ind_num){
  response_data_list[[i]] <- get_data(individual_list[[i]], TRUE)
}

temp_matrix <- matrix(nrow = ind_num*2+1, ncol = ind_num)
Response_time_vector <- c()
index_vector <- c()
facet_vector <- c()
temp <- c()
myplot <- NA
for(i in 1:obj_num){
  
  temp <- c(temp, myplot)
}
##########################
i <- 1
Response_time_vector <- c()
index_vector <- c()
facet_vector <- c()
for(j in 1:ind_num){
  Response_time_vector <- c(Response_time_vector, response_data_list[[j]][[i]])
  index_vector <- c(index_vector, rep(config_list[[j]], length(response_data_list[[j]][[i]])))
  facet_vector <- c(facet_vector, rep(objective_list[[i]], length(response_data_list[[j]][[i]])))
}
df <- data.frame(Response_time=Response_time_vector, Configurations=index_vector, ind2=facet_vector)
myplot1<-ggplot(df, aes(x=Configurations, y=Response_time, group=Configurations))+
  geom_violin(fill='lightblue', alpha=0.5)+
  geom_boxplot(width=0.075)+
  #geom_jitter(position = position_jitter(width = .1))+
  facet_wrap(~ ind2)+
  coord_cartesian(ylim=c(0,max(Response_time_vector)))+
  theme(text = element_text(family="serif", size=12))+
  ylab("Response time (MSec)") +
  xlab("Configurations")
###################################
# 
# i <- 2
# Response_time_vector <- c()
# index_vector <- c()
# facet_vector <- c()
# for(j in 1:ind_num){
#   Response_time_vector <- c(Response_time_vector, response_data_list[[j]][[i]])
#   index_vector <- c(index_vector, rep(config_list[[j]], length(response_data_list[[j]][[i]])))
#   facet_vector <- c(facet_vector, rep(objective_list[[i]], length(response_data_list[[j]][[i]])))
# }
# df <- data.frame(Response_time=Response_time_vector, Configurations=index_vector, ind2=facet_vector)
# myplot2<-ggplot(df, aes(x=Configurations, y=Response_time, group=Configurations))+
#   geom_boxplot()+
#   geom_violin(fill='lightblue', alpha=0.5)+
#   #geom_jitter(position = position_jitter(width = .1))+
#   facet_wrap(~ ind2)+
#   coord_cartesian(ylim=c(0,max(Response_time_vector)))+
#   theme(text = element_text(family="serif", size=20))

###################################
i <- 3
Response_time_vector <- c()
index_vector <- c()
facet_vector <- c()
for(j in 1:ind_num){
  Response_time_vector <- c(Response_time_vector, response_data_list[[j]][[i]])
  index_vector <- c(index_vector, rep(config_list[[j]], length(response_data_list[[j]][[i]])))
  facet_vector <- c(facet_vector, rep(objective_list[[i]], length(response_data_list[[j]][[i]])))
}
df <- data.frame(Response_time=Response_time_vector, Configurations=index_vector, ind2=facet_vector)
myplot3<-ggplot(df, aes(x=Configurations, y=Response_time, group=Configurations))+
  geom_violin(fill='lightblue', alpha=0.5)+
  geom_boxplot(width=0.075)+
  #geom_jitter(position = position_jitter(width = .1))+
  facet_wrap(~ ind2)+
  coord_cartesian(ylim=c(0,max(Response_time_vector)))+
  theme(text = element_text(family="serif", size=12))+
  ylab("Response time (MSec)") +
  xlab("Configurations")
###################################
i <- 4
Response_time_vector <- c()
index_vector <- c()
facet_vector <- c()
for(j in 1:ind_num){
  Response_time_vector <- c(Response_time_vector, response_data_list[[j]][[i]])
  index_vector <- c(index_vector, rep(config_list[[j]], length(response_data_list[[j]][[i]])))
  facet_vector <- c(facet_vector, rep(objective_list[[i]], length(response_data_list[[j]][[i]])))
}
df <- data.frame(Response_time=Response_time_vector, Configurations=index_vector, ind2=facet_vector)
myplot4<-ggplot(df, aes(x=Configurations, y=Response_time, group=Configurations))+
  geom_violin(fill='lightblue', alpha=0.5)+
  geom_boxplot(width=0.075)+
  #geom_jitter(position = position_jitter(width = .1))+
  facet_wrap(~ ind2)+
  coord_cartesian(ylim=c(0,max(Response_time_vector)))+
  theme(text = element_text(family="serif", size=12))+
  ylab("Response time (MSec)") +
  xlab("Configurations")
###################################
# i <- 5
# Response_time_vector <- c()
# index_vector <- c()
# facet_vector <- c()
# for(j in 1:ind_num){
#   Response_time_vector <- c(Response_time_vector, response_data_list[[j]][[i]])
#   index_vector <- c(index_vector, rep(config_list[[j]], length(response_data_list[[j]][[i]])))
#   facet_vector <- c(facet_vector, rep(objective_list[[i]], length(response_data_list[[j]][[i]])))
# }
# df <- data.frame(Response_time=Response_time_vector, Configurations=index_vector, ind2=facet_vector)
# myplot5<-ggplot(df, aes(x=Configurations, y=Response_time, group=Configurations))+
#   geom_boxplot()+
#   geom_violin(fill='lightblue', alpha=0.5)+
#   #geom_jitter(position = position_jitter(width = .1))+
#   facet_wrap(~ ind2)+
#   coord_cartesian(ylim=c(0,max(Response_time_vector)))+
#   theme(text = element_text(family="serif", size=20))
###################################
pdf("D:/filename.pdf", width = 10.5, height = 3) # Open a new pdf file
print(gridExtra::grid.arrange(myplot1,myplot3,myplot4, ncol=3))
dev.off()
#par(mfrow=c(2,3))
#pdf()
#g <- arrangeGrob(myplot1,myplot2,myplot3,myplot4,myplot5, nrow=2) #generates g
ggsave(file="whatever.pdf", g) #saves g
#g <- arrangeGrob(plot1, plot2, plot3, nrow=3) #generates g
#ggsave(file="whatever.pdf", g) #saves g


#df <- data.frame(response=Response_time_vector, ind=index_vector, ind2=facet_vector)
#myplot<-ggplot(df, aes(x=ind, y=response, group=ind))+
#  geom_boxplot()+
#  geom_violin(fill='lightblue', alpha=0.5)+
##  geom_jitter(position = position_jitter(width = .1))+
#  facet_grid(ind2 ~ ., scales="free")+
#  facet_wrap(~ ind2, ncol=2)
#print(myplot)
