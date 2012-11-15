#check first and second
#check difference between first and second or difference between two results

red_color<-"#C97F5F"
blue_color<-"#3E4875"

#setwd("/Users/administrator/code/js/chrome-study-tracker/analyze")
setwd("/Users/rhema/Documents/work/gitwork/chrome-study-tracker/analyze/survey")
likert_data<-read.csv('likerts_renamed.csv',header=TRUE)
metrics<-cbind('interesting', 'overview', 'overall', 'citations')

library(sciplot)


sums<-function(nothing)
{
   for(i in 1:length(metrics))
   {
      print(metrics[i])
      print(t.test(likert_data[metrics[i]]-5))
   }
}

graph_idiation<-function(ideation_names,y_max,xoff)
{
   print(ideation_names)
   names<-c()
   dats<-NULL
   for(i in 1:length(ideation_names))
   {
      cname<-gsub(pattern = "\\ ", replacement = ".", ideation_names[i])
      print(cname)
      fall_numbers = likert_data[cname]
      fall_numbers<-subset(fall_numbers, fall_numbers>=0)
      fnums<-cbind("fall",ideation_names[i],fall_numbers)
      names(fnums)<-c("semester","metric","score")
      dats<-(rbind(dats,fnums))
   }
   dats$score = dats$score - 5
   print(dats)
   bargraph.CI(metric, score, data = dats, cex.lab = 1.5, x.leg = xoff, cex.leg = 1.5, angle = 45, cex.names = 1.7, cex.axis = 1.7, col=c(red_color),ylim=c(-4,4), legend = TRUE)
   return(dats)
}




pdf("likert.pdf",width=9,height=5,4)
x<-graph_idiation(metrics)
dev.off()

pdf("boxp.pdf",width=7,height=4,4)
plot(x$metric,x$score)
dev.off()

sums()





