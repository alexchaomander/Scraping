setwd("~/Dropbox/Scraping/samuelTwitterProject")

mapping = read.csv("uniqueUserDF.csv", header = T)
actual = read.csv('modified.csv', header = T)
actual = actual[,2:5]
mapping = mapping[,3:5]

for (i in 1:nrow(actual)) {
  print(i)
  for (j in 1:nrow(mapping)) {
    if (actual$Username[i] == mapping$uniqueUsers[j]) {
      actual$Number.of.Followers = mapping[mapping$uniqueUser == actual$Username[i], 2]
      actual$Number.of.Mentions = mapping[mapping$uniqueUser == actual$Username[i], 3]
    }
  }
}

a = merge(actual, mapping, by.x = "Username", by.y = "uniqueUsers")
actual$Number.of.Followers = a$numFollowers
actual$Number.of.Mentions = a$numMentions
write.csv(actual, 'modified.csv')
