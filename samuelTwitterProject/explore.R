setwd("~/Dropbox/Scraping/samuelTwitterProject")
# twitterdata = read.csv("I21c_twitterdata.csv", header=T)
twitterdata = read.csv('modified.csv', header=T)
uniqueUserDF = read.csv('uniqueUserDF.csv', header=T)

odd  = function(x) x %% 2 != 0 
even = function(x) x %% 2 == 0 
evenb = function(x) !odd(x) 


require(twitteR)
require(plyr)
twitterdata$URL = as.character(twitterdata$URL)
usernames = strsplit(twitterdata$URL, "http://twitter.com/")
usernames = unlist(usernames)
usernames = usernames[even(1:length(usernames))]
usernames = strsplit(usernames, "/statuses")
usernames = unlist(usernames)
usernames = usernames[odd(1:length(usernames))]
twitterdata$Username = usernames

#Getting number of followers
for (i in 501:550) {
  user = twitterdata$Username[i]
  a = try(getUser(user), silent = T)
  if (class(a) == "try-error") {
    twitterdata$Number.of.Followers[i] = NA
  } else {
    twitterdata$Number.of.Followers[i] = a$followersCount
  }
}

#he # of times each specific user mentions the company "ISRAEL21c
for (i in 1:20) {
  if (is.na(twitterdata$Number.of.Followers[i])) {
    twitterdata$Number.of.Mentions = NA
  } else {
    user = twitterdata$Username[i]
    timeline = try(userTimeline(user, n=20, includeRts = T, excludeReplies = F), silent = T)
    df = do.call("rbind", lapply(timeline, as.data.frame))
    twitterdata$Number.of.Mentions[i] = length(grep('ISRAEL21c', df$text))
  }
}

uniqueUsers = unique(twitterdata$Username)
numFollowers = rep(x = 0, times = length(uniqueUsers))
numMentions = rep(x = 0, times = length(uniqueUsers))
uniqueUserDF = data.frame(uniqueUsers, numFollowers, numMentions, stringsAsFactors = F)

for (i in 11036:nrow(uniqueUserDF)) {
  print(i)
  user = uniqueUserDF$uniqueUsers[i]
  a = try(getUser(user), silent = T)
  if (class(a) == "try-error") {
    uniqueUserDF$numFollowers[i] = NA
    uniqueUserDF$numMentions[i] = NA
  } else {
    uniqueUserDF$numFollowers[i] = a$followersCount
    timeline = try(userTimeline(user, n=100, includeRts = T, excludeReplies = F), silent = T)
    df = do.call("rbind", lapply(timeline, as.data.frame))
    uniqueUserDF$numMentions[i] = length(grep('ISRAEL21c', df$text))
  }
}
#3000-4000
#10001-nrow(uniqueUserDF)
write.csv(uniqueUserDF, 'uniqueUserDF_mac.csv')



setup_twitter_oauth(consumer_key = "YOUR KEY HERE",
                    consumer_secret = "YOUR KEY HERE",
                    access_token = "YOUR KEY HERE",
                    access_secret = "YOUR KEY HERE")