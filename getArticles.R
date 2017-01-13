#!/usr/bin/Rscript
#install.packages("tidyr",repos="https://cran.wu.ac.at/")
#install.packages("stringi",repos="https://cran.wu.ac.at/")
#install.packages("gutenbergr",repos="https://cran.wu.ac.at/")

library('dplyr')
library('gutenbergr')
library('tidyr')

authors<-c('Dickens, Charles','Kafka, Franz','Carroll, Lewis', 'Twain, Mark', 'Joyce, James', 'Wilde, Oscar', 'Plato', 'Dostoyevsky, Fyodor', 'Alighieri, Dante', 'Shakespeare, William', 'Homer', 'Defoe, Daniel', 'Christie, Agatha', 'Flaubert, Gustave', 'Einstein, Albert', 'Asimov, Isaac', 'London, Jack', 'Ibsen, Henrik'   )
for (a in authors){
	authors_books <- gutenberg_works(author == a) %>%
  		gutenberg_download(meta_fields = "title",mirror='ftp://sunsite.informatik.rwth-aachen.de/pub/mirror/ibiblio/gutenberg')
	authors_books
}