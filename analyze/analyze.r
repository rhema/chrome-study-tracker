#check first and second
#check difference between first and second or difference between two results
setwd("/Users/administrator/code/js/chrome-study-tracker/analyze")
fluency<-read.csv('first.csv',header=TRUE)

aov.result <- aov(collected ~ dataset*method, data=fluency)
summary(aov.result)
model.tables(aov.result, "means")