##### INSTALLING PACKAGES #####
install.packages(c("tm", "SnowballC", "wordcloud", "proxy", "kernlab", "NLP", "openNLP"))
nstall.packages("openNLPmodels.en", repos="http://datacube.wu.ac.at/", type="source")

##### LOADING LIBRARIES #####
library(proxy)
library(tm)
library(proxy)
library(kernlab)
library(NLP)
library(openNLP)
 # Framework for text mining.
library(SnowballC)
 # Provides wordStem() for stemming.
#library(qdap)
 # Quantitative discourse analysis of transcripts.
#library(qdapDictionaries)library(dplyr)
 # Data preparation and pipes %>%.
#library(RColorBrewer)
 # Generate palette of colours for plots.
#library(ggplot2)
 # Plot word frequencies.
#library(scales)
 # Include commas in numbers.
#library(Rgraphviz)
 # Correlation plots.

##### LOADING CORPUS #####
cname <- file.path("/home/matic/Dropbox/Inteligentni Sistemi/Assigment2/","articles")
length(dir(cname))
corpus <- Corpus(DirSource(cname))
#summary(corpus)
#inspect(corpus[16])

##### TRANSFORMING TEXT #####
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CE ZELIMO KLASIFICIRATI AVTORJA BESEDILA, POTEM JE LAHKO TUDI RABA VEZNIKOV/'STOPWORDS' POMEMBNA IN KONCNICE BESED RAVNO TAKO
#PREDLAGAM, DA SE NEKATERE TRANSFORMACIJE IZVEDE NAD TEXTOM SAMO ZA NAMEN TVORBE STATISTICNIH ATRIBUTOV KOT NPR. TF-IDF...
# Change letters to lower case
corpus <- tm_map(corpus, content_transformer(tolower))
# Remove punctuations
corpus <- tm_map(corpus, removePunctuation)
# Remove numbers
corpus <- tm_map(corpus, removeNumbers)
# Remove stopwords (these are some of the most common, short function words, such as the, is, at, which, etc.)
corpus <- tm_map(corpus, removeWords, stopwords('english'))
# Stem words to retrieve their radicals, so that various forms derived from a stem would be taken as the same 
# when counting word frequency
corpus <- tm_map(corpus, stemDocument)
# Strip extra whitespace from text documents
corpus <- tm_map(corpus, stripWhitespace)
# Have a look at the first document in the corpus
content(corpus[[1]])

##### TERM-DOCUMENT MATRIX #####
# A term-document matrix represents the relationship between terms and documents, 
# where each row stands for a term and each column for a document, and an entry 
# is the number of occurrences of the term in the document.
tdm <- TermDocumentMatrix(corpus)
tdm
# Retrieve the list of terms
rownames(tdm)
# Find the term "moscow"
#idx <- which(rownames(tdm) == "moscow")
#idx
# Have a look at the term "moscow" in the documents
#inspect(tdm[idx,])

##### FREQUENT TERMS #####
# Inspect frequent words (with frequency no less than 300)
findFreqTerms(tdm, lowfreq=300)
# The barplot shows the most frequent words in the corpus
termFrequency <- rowSums(as.matrix(tdm))
termFrequency <- subset(termFrequency, termFrequency >= 300)
barplot(termFrequency)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TERM FREQUENCY IMAMO ------> POTREBUJEMO SE INVERSE DOCUMENT FREQUENCY ZA PREPOZNAVO POMEMBNIH BESED ( NJIHOVE POGOSTOSTI UPORABI KOT ATRIBUTE )
# A word cloud is a visual representation for text data. 
# Tags are single words, and the importance of each tag is shown with font size and color.
library(wordcloud)
# Convert the term-document matrix to a normal matrix and calculate word frequencies
mat <- as.matrix(tdm)
wordFreq <- sort(rowSums(mat), decreasing=TRUE)
grayLevels <- gray((wordFreq+10) / (max(wordFreq)+10))
wordcloud(words=names(wordFreq), freq=wordFreq, min.freq=100, random.order=F, colors=grayLevels)

##### ASSOCIATIONS #####
# Find terms associated with "moscow" with correlation no less than 0.5
findAssocs(tdm, "moscow", 0.5)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KORELIRANOST GLEDE NA KAJ?- STEVILO POJAVITEV SKOZI DOKUMENTE?


##### CLUSTERING OF WORDS ##### 
# Remove sparse terms that have at least 70% of empty elements
tdm2 <- removeSparseTerms(tdm, sparse=0.7)
mat <- as.matrix(tdm2)
# The distances between terms can also be calculated using the dist() function
distMatrix <- dist(mat)
# Find clusters of words with hierarchical clustering
fit <- hclust(distMatrix, method="ward.D")
plot(fit)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ZGOLJ ALTERNATIVA KORELACIJI?

##### CLUSTERING OF DOCUMENTS #####
# Constructs a document-term matrix
dtm <- DocumentTermMatrix(corpus, control = list(weighting=weightTfIdf))
mat <- as.matrix(dtm)
# Cluster the documents using the kmeans method with the number of clusters set to 3 
k <- 3
kmeansResult <- kmeans(mat, k)
# Find the most popular words in every cluster
for (i in 1:k) 
{
	s <- sort(kmeansResult$centers[i,], decreasing=T)
	cat(names(s)[1:10], "\n")
}


##### DOCUMENT DISTANCE #####
# Compute the dissimilarity between the first two documents using the cosine distance measure.
# Cosine similarity is a measure of similarity between two vectors of an inner product space that measures the cosine of the angle between them.
# Each term represents a different dimension and a document is characterised by a vector where the value of each dimension corresponds to 
# the number of times that term appears in the document. Cosine similarity then gives a useful measure of how similar two documents are likely
# to be in terms of their subject matter.
library(proxy)
content(corpus[[1]])
content(corpus[[2]])
dist(as.matrix(dtm)[c(1,2),], method = "cosine")
# Find the most similar documents in the term-document matrix (this may take a few moments to compute...)
dtm2 <- removeSparseTerms(dtm, sparse=0.8)
mat <- as.matrix(dtm2)
dist.mat <- as.matrix(dist(mat, method = "cosine"))
sim.idx <- which(dist.mat == min(dist.mat[dist.mat > 0]), arr.ind = TRUE)
sim.idx
# Have a look at these documents
content(corpus[[sim.idx[1,1]]])
content(corpus[[sim.idx[1,2]]])
dist(mat[c(sim.idx[1,1], sim.idx[1,2]),], method = "cosine")
