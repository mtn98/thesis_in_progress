# Load libraries
#install.packages("devtools") 
library(devtools)
#install_github("gandalfnicolas/SADCAT")

library(SADCAT)
library(dplyr)
library(tidyr)

Pre_Dictionaries = SADCAT::All.steps_Dictionaries

# View the structure
#str(Pre_Dictionaries)
#see first rows 
#head(Pre_Dictionaries)
#view the entire dataframe
#View(Pre_Dictionaries)
#view the column names
#colnames(Pre_Dictionaries)

Pre_Dictionaries$values0 = as.character(Pre_Dictionaries$tv)

Pre_Dictionaries$values0 <- enc2utf8(as.character(Pre_Dictionaries$values0))

Pre_Dictionaries$values0 = tolower(Pre_Dictionaries$values0) #transform to lower case
write.csv(Pre_Dictionaries, "SADCAT_dictionaries.csv", row.names = FALSE)



