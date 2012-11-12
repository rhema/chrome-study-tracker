#check first and second
#check difference between first and second or difference between two results

setwd("/Users/administrator/code/js/chrome-study-tracker/analyze")
study_data<-read.csv('first.csv',header=TRUE)
metrics<-cbind('collected','total_time','pdf_time','paper_page_time','start_page_time','collecting_time','transitional_page_time','depth_mean','depth_max', 'collected_depth','page_impression','keyword_variety','collection_novelty')

between_subjects_tests <- function()
{
  for(i in 1:length(metrics))
  {
    print(metrics[i])
    aov.result <- aov(study_data[,metrics[i]] ~ study_data[,'dataset']*study_data[,'method'])
    print(summary(aov.result))
    print(model.tables(aov.result, "means"))  
  }
}

within_subjects_tests <- function()
{
  for(i in 1:length(metrics))
  {
    print("Start...")
    print(metrics[i])
    aov.result <- aov(study_data[,metrics[i]] ~ study_data[,'method']+Error(study_data[,'subject']/study_data[,'method']))
    print(summary(aov.result))
    print(model.tables(aov.result, "means"))
    print("end")
    print("") 
  }
}


###by hands
# cor.test(study_data[,'collected'], study_data[,'depth_max']) shows positive correlation between the number collected and the max depth....
#
#
#found thus fars...
#########################ice     web
#'collected'      ,         10.714 12.000 
#'total_time',              21.817 21.201 
#'pdf_time',                0.8495 0.7620 
#'paper_page_time',         0.789 16.237  ***
#'start_page_time',         18.735  2.476  ***
#'collecting_time',         0.8842 1.2541   (p 0.1070)
#'transitional_page_time',  0.0306 0.9057 *
#'depth_mean',           ,  2.1740 2.4872
'depth_max'                 4.143 5.286
#'collected_depth',         2.2479 1.9810  (p .4393)
#'page_impression'          37.57 34.64
####################
##tested separating grad from non grad students, found no difference