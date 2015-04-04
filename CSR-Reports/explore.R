## Reading in text files into R
currentDirectory = "~/Desktop/PCR_text"
setwd(currentDirectory)
source("~/Desktop/ClusteringCrowdfunding/createTDM.R")
source("~/Desktop/ClusteringCrowdfunding/createWordCloud.R")
source("~/Desktop/ClusteringCrowdfunding/createGramFrequency.R")
allFiles = list.files("corpus/", recursive = T)

wordCloudCreator = function(filePath, ngrams) {
  f = paste("corpus/", filePath, sep="")
  a = readChar(f, file.info(f)$size)
  corpus = data.frame(Words = a, stringsAsFactors = F)
  fullPath = strsplit(filePath, "/")
  company = fullPath[[1]][1]
  corpusName = fullPath[[1]][2]
  directory = paste("clouds/", company, sep="")
  dir.create(paste(currentDirectory, directory ,sep = ""), showWarnings = FALSE)
  png(filename=paste("clouds/", company, "/", corpusName, "_", "Cloud", "_", ngrams,"-gram", sep=""))
  createWordCloud(corpus$Words, "text", ngrams)
  dev.off()
}

gramFrequencyCreator = function(filePath, ngrams) {
  f = paste("corpus/", filePath, sep="")
  a = readChar(f, file.info(f)$size)
  corpus = data.frame(Words = a, stringsAsFactors = F)
  TDM = createTDM(corpus$Words, "text", ngrams)
  m = as.matrix(TDM)
  v = sort(rowSums(m),decreasing=TRUE)
  d = data.frame(Gram = names(v),Frequency=v)
  row.names(d) = NULL
  return(d)
}


for (i in 1:length(allFiles)) {
  for (j in 1:2) {
    
    #Creating the word clouds
    try(wordCloudCreator(allFiles[i], j))
    
    #Creating the gram frequency tables
    fullPath = strsplit(allFiles[i], "/")
    company = fullPath[[1]][1]
    corpusName = fullPath[[1]][2]
    directory = paste("gramFrequency/", company, sep="")
    dir.create(paste(currentDirectory, directory, sep = ""), showWarnings = FALSE)
    fileName = paste("gramFrequency/", company, "/", corpusName, "_", j, "-Gram", "_", "Frequency.csv", sep = "")
    write.csv(gramFrequencyCreator(allFiles[i], j), file = fileName)
  }
}


#TDM = createTDM(corpus, "text", 2)
#createWordCloud(corpus$Words, "text", 2)

# TDM_common = removeSparseTerms(TDM, sparse = 0.99)
# # numTerms = dim(TDM_common)[1]
# # inspect(TDM_common[1:numTerms, 1:10])
# 
# TDM_common = as.matrix(TDM_common)
# # Cluster Dendogram of Successful BusTechWords Perk Descriptions
# plot(hclust(dist(TDM_common)), xlab="Words" , main = "Cluster Dendogram for Successful BusTech Perk Descriptions")

