install.packages("stringi","gutenbergr","tidyr")
install.packages()

library('dplyr')
library('gutenbergr')
library('tidyr')

gutenberg_works(title == "Wuthering Heights")
wuthering_heights <- gutenberg_download(768)
wuthering_heights