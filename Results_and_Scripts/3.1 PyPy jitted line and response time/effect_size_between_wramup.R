library("rjson")
library("effsize")

result_root = ''
benchmarks = c('ai', 'bm_mako', 'chaos', 'django', 'html5lib', 'pidigits', 'rietveld')

for(index in 1:length(benchmarks)){
  benchmark <- benchmarks[index]
  before_warmup <- read.csv(file = paste(result_root, benchmark, '_warming_up.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')[[3]]
  after_warmup <- read.csv(file = paste(result_root, benchmark, '_warmed_up.csv', sep=''), header=FALSE, stringsAsFactors = FALSE, sep=',')[[3]]
  
  list_A <- as.numeric(before_warmup)
  list_B <- as.numeric(after_warmup)
  wilcox_sum <- wilcox.test(list_A, list_B, paired=FALSE)
  cliff <- cliff.delta(list_A, list_B)
  print(benchmark)
  print(wilcox_sum$p.value)
  print(cliff$estimate)
}
