input_file <- paste('scale05_coverage.csv', sep='')

csv_data1 <- read.csv(file=input_file,head=FALSE,sep=",")

input_file <- paste('scale06_coverage.csv', sep='')

csv_data2 <- read.csv(file=input_file,head=FALSE,sep=",")

input_file <- paste('scale08_coverage.csv', sep='')

csv_data3 <- read.csv(file=input_file,head=FALSE,sep=",")

mem_data <- c(as.numeric(csv_data1[[3]]),as.numeric(csv_data2[[3]]))#,as.numeric(csv_data3[[3]]))
line_data <- c(as.numeric(csv_data1[[2]]),as.numeric(csv_data2[[2]]))#,as.numeric(csv_data3[[2]]))

y1 = c(1,2,3,4,5)
x1 = c(2,4,6,8,10)

y2 = c(1,2,3,4,5)
x2 = c(10,20,30,40,50)

#mem_data <- c(y1, y2)
#line_data <- c(x1, x2)
print(length(mem_data))
print(length(line_data))
mem <- mem_data#as.numeric(csv_data[[3]])
line_num <- line_data#as.numeric(csv_data[[2]])

#result = cor(x=mem,y=line_num,method = 'pearson')
#print(result)

result = cor.test(x=mem,y=line_num,method = 'spearman', exact = TRUE)
print(result)
