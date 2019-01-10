library('ggplot2')
input_file <- paste('saleor/saleor_jitted_response_decoded.csv', sep='')
#input_file <- paste('wagtail/wagtail_jitted_response_decoded.csv', sep='')
#input_file <- paste('quokka/quokka_jitted_response_decoded.csv', sep='')
20
13
11
index_line = 20

csv_data <- read.csv(file=input_file,head=FALSE,sep=",")


response <- as.numeric(csv_data[[index_line]])
line <- as.numeric(csv_data[[7]])

df <- data.frame(line, response,xmin=10230, xmax=10550, ymin=1400, ymax=2861)

ggplot(df, aes(x = line, y = response)) +
# ???????????????
  geom_line()+
  geom_point()+
  geom_point(aes(x=1285, y=6229), colour="red", size=3)+
  geom_hline(yintercept=4652, linetype="dashed", color = "red", size=1)+
  geom_text(aes(x=1285-30, y=6229+300, label='A'), size=4)+
  #geom_rect(aes(xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax), alpha=0.002, fill="red")+
  #geom_text(aes(x=xmin, y=ymax+200, label='A'), size=4)+
  #geom_text(aes(x=xmax+200, y=ymin+340, label='B'), size=4)+
  theme(text = element_text(family="serif", size=12))+
  ylab("Response time (MSec)") +
  xlab("Number of jitted lines")
