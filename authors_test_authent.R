#!/usr/bin/Rscript
#install.packages("tidyr",repos="https://cran.wu.ac.at/")
#install.packages("stringi",repos="https://cran.wu.ac.at/")
#install.packages("gutenbergr",repos="https://cran.wu.ac.at/")

library('dplyr')
library('gutenbergr')
library('tidyr')

authors<-c('Dickens, Charles','Carroll, Lewis', 'Twain, Mark', 'Joyce, James', 'Wilde, Oscar', 'Plato', 'Dostoyevsky, Fyodor', 'Shakespeare, William', 'Homer', 'Defoe, Daniel', 'Christie, Agatha', 'Flaubert, Gustave', 'Einstein, Albert', 'Asimov, Isaac', 'London, Jack', 'Ibsen, Henrik', 'Austen, Jane', 'Rand, Ayn', 'Tyler, Anna Cogswell', 'Shelley, Mary Wollstonecraft', 'Eliot, George', 'Chopin, Kate', 'Brontë, Emily', 'Alcott, Louisa May', 'Wharton, Edith', 'West, Rebecca', 'Woolf, Virginia', 'Cather, Willa', 'Rand, Ayn' )
#go through all authors
for (a in authors){
	print(a)
	print(gutenberg_works(author == a))	
}