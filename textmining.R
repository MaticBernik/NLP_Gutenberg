##### INSTALLING PACKAGES #####
install.packages(c("tm", "SnowballC", "wordcloud", "proxy", "kernlab", "NLP", "openNLP"))
install.packages("openNLPmodels.en", repos="http://datacube.wu.ac.at/", type="source")

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
#cname <- file.path("C:/Users/Robert/Desktop/IS_local_test/NLP_Gutenberg","articles")

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
wordcloud(words=names(wordFreq), freq=wordFreq, min.freq=100, random.order=F, colors=brewer.pal(6, "Dark2")), max.words=500)

##### ASSOCIATIONS #####
# Find terms associated with "moscow" with correlation no less than 0.5
findAssocs(tdm, "moscow", 0.5)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KORELIRANOST GLEDE NA KAJ?- STEVILO POJAVITEV SKOZI DOKUMENTE?


##### CLUSTERING OF WORDS ##### 
# Remove sparse terms that have at least 70% of empty elements
tdm2 <- removeSparseTerms(tdm, sparse=0.7)
mat <- as.matrix(tdm2)
write.csv(m, file="documentTermFrequency.csv")
# The distances between terms can also be calculated using the dist() function
distMatrix <- dist(mat)
# Find clusters of words with hierarchical clustering
fit <- hclust(distMatrix, method="ward.D")
plot(fit)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ZGOLJ ALTERNATIVA KORELACIJI? - ISTI NAMEN?

##### CLUSTERING OF DOCUMENTS #####
# Constructs a document-term matrix
dtm <- DocumentTermMatrix(corpus, control = list(weighting=weightTfIdf))
mat <- as.matrix(dtm)
# Cluster the documents using the kmeans method with the number of clusters set to 3 
k <- 27
kmeansResult <- kmeans(mat, k)
# Find the most popular words in every cluster
for (i in 1:k) 
{
	s <- sort(kmeansResult$centers[i,], decreasing=T)
	cat(names(s)[1:10], "\n")
}





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


#
#
# Document classification
#
#

# Construct a corpus for a directory as source. Each file in this directory is considered to be a document.
corpus <-Corpus(DirSource("economy"))

length(corpus )


# Corpus preprocessing
corpus  <- tm_map(corpus , removeNumbers)
corpus  <- tm_map(corpus , removePunctuation)
corpus  <- tm_map(corpus , content_transformer(tolower))
corpus  <- tm_map(corpus , removeWords, stopwords())
corpus  <- tm_map(corpus , stemDocument)
corpus  <- tm_map(corpus , stripWhitespace)


#
# Transforming the corpus into a data set
#

# Construct a document-term matrix
data.tfidf <- DocumentTermMatrix(corpus, control = list(weighting=weightTfIdf))

# Read the document classes
Topic <-read.table("economy-topics.txt")

# Construct a data set
data <- cbind(as.matrix(data.tfidf), Topic)
names(data)[ncol(data)] <- "Topic"


sel <- sample(nrow(data), 200, F)
train <- data[-sel,]
test <- data[sel,]


#
# Document classification using kNN models
#

library(class)

# Identify the class column
r <- which(names(data)=="Topic")

predicted <- knn(train[,-r], test[,-r], train$Topic)
observed <- test$Topic
t <- table(observed, predicted)
t

# Classification accuracy
sum(diag(t))/sum(t)

# Recall is the fraction of relevant instances that are retrieved (here calculated for the class "general")
t[1,1]/sum(t[1,])

# Precision is the fraction of retrieved instances that are relevant (here calculated for the class "general") 
t[1,1]/sum(t[,1])



#
# Document classification using SVM
#

library(kernlab)

# svm with a radial basis kernel
model.svm <- ksvm(Topic ~ ., train, kernel = "rbfdot")
predicted <- predict(model.svm, test, type = "response")
t <- table(observed, predicted)
t

# Classification accuracy
sum(diag(t))/sum(t)

# Recall (here calculated for the class "general")
t[1,1]/sum(t[1,])

# Precision (here calculated for the class "general")
t[1,1]/sum(t[,1])


# svm with a polynomial kernel
model.svm <- ksvm(Topic ~ ., train, kernel = "poly", kpar=list(degree=2))
predicted <- predict(model.svm, test, type = "response")
t <- table(observed, predicted)
t

# Classification accuracy
sum(diag(t))/sum(t)

# Recall is the fraction of relevant instances that are retrieved (here calculated for the class "general")
t[1,1]/sum(t[1,])

# Precision is the fraction of retrieved instances that are relevant (here calculated for the class "general") 
t[1,1]/sum(t[,1])



#
# Tokenization, sentence segmentation, part-of-speech tagging
#

library(NLP)
library(openNLP)
#library(openNLPmodels.en)


s <- "Steven Allan Spielberg is an American filmmaker and business magnate. Spielberg is consistently considered as one of the leading pioneers of the New Hollywood era, as well as being viewed as one of the most popular and influential filmmakers in the history of cinema."
s <- as.String(s)

# Generate an annotator which computes sentence annotations 
sent_ann <- Maxent_Sent_Token_Annotator()
sent_ann
a1 <- annotate(s, sent_ann)
a1

# Extract sentences
s[a1]


# Generate an annotator which computes word token annotations
word_ann <- Maxent_Word_Token_Annotator()
word_ann
a2 <- annotate(s, word_ann, a1)
a2

# Extract words
a2w <- subset(a2, type == "word")
s[a2w]


# Generate an annotator which computes POS tag annotations
pos_ann <- Maxent_POS_Tag_Annotator()
pos_ann
a3 <- annotate(s, pos_ann, a2)
a3

# Part of Speech labels
#
# NN - Noun
# NNP - Proper noun
# NNS - Noun, plural
# VB - Verb
# VBD - Verb, past tense
# VBG - Verb, gerund or present participle
# VBN - Verb, past participle
# VBP - Verb, non­3rd person singular present
# VBZ - Verb, 3rd person singular present 
# DT - Determiner
# JJ - Adjective
# JJR - Adjective, comparative
# JJS - Adjective, superlative
# IN - Preposition or subordinating conjunction
# PRP - Personal pronoun 
# RB - Adverb
# RBR - Adverb, comparative
# RBS - Adverb, superlative 
# CC - Conjunction
# CD - Cardinal number
# ...
 

 
a3w <- subset(a3, type == "word")
a3w

# Extract token/POS pairs

tags <- vector()
for (i in 1:length(a3w$features))
	tags <- c(tags, a3w$features[[i]]$POS)

table(tags)


tokenPOS <- cbind(s[a3w], tags)
tokenPOS

# Identify all nouns in the text
tokenPOS[substr(tokenPOS[,2], 1, 2) == "NN", 1]

# Identify all verbs in the text
tokenPOS[substr(tokenPOS[,2], 1, 2) == "VB", 1]

# Identify all adjectives in the text
tokenPOS[substr(tokenPOS[,2], 1, 2) == "JJ", 1]


#
# Entity recognition for persons, dates, locations, and organizations 
#

s <- "LeBron Raymone James (born on December 30, 1984, in Akron, Ohio) is an American professional basketball player for the Cleveland Cavaliers of the National Basketball Association (NBA)."
s <- as.String(s)

sent_ann <- Maxent_Sent_Token_Annotator()
word_ann <- Maxent_Word_Token_Annotator() 
person_ann <- Maxent_Entity_Annotator(kind = "person")
date_ann <- Maxent_Entity_Annotator(kind = "date")
location_ann <- Maxent_Entity_Annotator(kind = "location")
organization_ann <- Maxent_Entity_Annotator(kind = "organization")


ann <- annotate(s, list(sent_ann, word_ann, person_ann, date_ann, location_ann, organization_ann))
ann


entities <- function(annots, kind) 
{
	k <- sapply(annots$features, `[[`, "kind")
    	s[annots[k == kind]]
}

entities(ann, "person")
entities(ann, "date")
entities(ann, "location")
entities(ann, "organization")

