import os
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import wordnet
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
import numpy as np
import matplotlib.pyplot as plt
#nltk.download() #<- ODKOMENTIRAJ CE POGANJAS PRVIC!
print('***Predviden cas izvajanja je ~9min')
#METODI ZA 'STOPANJE' CASA ^^
def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print ("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")


#projectDir = "/home/matic/Dropbox/Inteligentni Sistemi/Assigment2/"
projectDir = "C:/Users/Robert/Desktop/IS_local/NLP_Gutenberg/"

os.chdir(projectDir)
#Atributi izpeljani iz stevila pojavitev znakov znotraj dokumenta so pretvorjeni v frekvence znotraj istega dokumenta
#---> nacin normalizacije zaradi neenakomerne dolzine clankov

#Tabela podatkov o avtorjih <--- trenutno veljaven samo spol
authors={'Eliot' : {'first name':'George', 'last name':'Eliot', 'gender':'F', 'period':'victorian', 'occupation':'novelist', 'nationality':'england'},
         'Chopin' : {'first name':'Kate', 'last name':'Chopin', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'Austen' : {'first name':'Austen', 'last name':'Jane', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'Woolf': {'first name':'Virginia', 'last name':'Woolf', 'gender':'F', 'period':'modernism', 'occupation':'novelist','nationality':'england'},
         'London': {'first name':'Jack', 'last name':'London', 'gender':'M', 'period':'victorian', 'occupation':'novelist', 'nationality':'america'},
         'Joyce': {'first name':'James', 'last name':'Joyce', 'gender':'M', 'period':'modern', 'occupation':'novelist', 'nationality':'ireland'},
         'Homer': {'first name':'Homer', 'last name':'', 'gender':'M', 'period':'ancient', 'occupation':'novelist'},
         'Einstein': {'first name':'Albert', 'last name':'Einstein', 'gender':'M', 'period':'victorian', 'occupation':'physicist'},
         'Defoe': {'first name':'Daniel', 'last name':'Defoe', 'gender':'M', 'period':'victorian', 'occupation':'novelist'},
         'Carroll': {'first name':'Lewis', 'last name':'Carroll', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'Asimov': {'first name':'Isaac', 'last name':'Asimov', 'gender':'M', 'period':'victorian', 'occupation':'novelist'},
         'Alcott': {'first name':'Louisa', 'last name':'Alcott', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'Plato': {'first name':'Plato', 'last name':'', 'gender':'M', 'period':'ancient greece', 'occupation':'novelist'},
         'Ibsen': {'first name':'Henrik', 'last name':'Ibsen', 'gender':'M', 'period':'natiralism | realism', 'occupation':'novelist'},
         'Wilde': {'first name':'Oscar', 'last name':'Wilde', 'gender':'M', 'period':'victorian', 'occupation':'author','nationality':'ireland'},
         'Wharton': {'first name':'Edith', 'last name':'Wharton', 'gender':'F', 'period':'naturalism', 'occupation':'novelist','nationality':'america'}, #New York
         'Tyler': {'first name':'Anna', 'last name':'Tyler', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'Twain': {'first name':'Mark', 'last name':'Twain', 'gender':'M', 'period':'victorian', 'occupation':'novelist'},
         'Rand': {'first name':'Ayn', 'last name':'Rand', 'gender':'F', 'period':'victorian', 'occupation':'writer'},
         'Dostoyevsky': {'first name':'Fyodor', 'last name':'Dostoyevsky', 'gender':'M', 'period':'victorian', 'occupation':'novelist', 'nationality': 'russian', 'movement': 'realism'},
         'Dickens': {'first name':'Charles', 'last name':'Dickens', 'gender':'M', 'period':'victorian', 'occupation':'novelist'},
         'Cather': {'first name':'Willa', 'last name':'Cather', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'West': {'first name':'Rebecca', 'last name':'West', 'gender':'F', 'period':'victorian', 'occupation':'novelist','nationality':'british'},
         'Shelley': {'first name':'Shalley', 'last name':'Mary', 'gender':'F', 'period':'victorian', 'occupation':'novelist'},
         'Shakespeare': {'first name':'William', 'last name':'Shakespeare', 'gender':'M', 'period':'elizabethian', 'occupation':'playwright', 'nationality':'english', 'movement': 'english renaissance'},
         'Flaubert': {'first name':'Gustave', 'last name':'Flaubert', 'gender':'M', 'period':'realism | romanticism', 'occupation':'novelist', 'nationality': 'french', 'movement': 'realism | romanticism'},
         'Christie': {'first name':'Agatha', 'last name':'Christie', 'gender':'F', 'period':'victorian', 'occupation':'novelist'}
         }

#Predpriprave na procesiranje texta
stemmer = nltk.stem.PorterStemmer()
punkt_param = PunktParameters()
sentence_splitter = PunktSentenceTokenizer(punkt_param)
toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)

articles={}
##### OBDELAVA CLANKOV #####
print("***Zacetek obdelave clankov")
tic()
for author in os.listdir("articles/"): #iterate trough authors
    if os.path.isdir(projectDir+'articles/'+author):
        for article in os.listdir('articles/'+author):
            with open('articles/'+author+'/'+article,'r') as file:
                text = file.read()
                text = text.lower() #text to lower case
            words = toker.tokenize(text)
            words_stemmed = [stemmer.stem(word) for word in words]
            words_stemmed_count = Counter(words_stemmed)
            tokens = nltk.word_tokenize(text) #tokenize text
            tokens_stemmed = [stemmer.stem(token) for token in tokens]
            tokens_stemmed_count = Counter(tokens_stemmed)
            sentences = sentence_splitter.tokenize(text)
            #number_words = sum(stem_noPunctuations_count.values())
            #number_spaces = text.count(' ')
            #number_tokens_withSpaces=sum(stem_count.values())+number_spaces
            #number_sentences = len(sentences)
            articles[article]={'author' : author,'content' : text,'words' : words_stemmed_count,'tokens' : tokens_stemmed_count,'sentences' : sentences}

def add_dictionaries(a,b):
    return dict((n, a.get(n, 0) + b.get(n, 0)) for n in set(a) | set(b))


##### GLOBALNA OBDELAVA CLANKOV #####
#Proceseranje clankov na globalni ravni
#boljsi pristop sestevanja slovarjev vseh clankov  ali  sesteti vse clanke v en string in ga loceno sprocesirati?? --> stopaj?
toc()
print("***Zacetek Globalne obdelave")
tic()
'''
#Pristop 1
global_words={}
global_tokens={}
global_sentences=[]
for article in articles:
    article_val=articles[article]
    global_words=add_dictionaries(global_words,article_val['words'])
    global_tokens=add_dictionaries(global_tokens,article_val['tokens'])
    global_sentences.extend(article_val['sentences'])'''

#Pristop2
global_text = ""
for article in articles:
    article=articles[article]
    global_text+=' '+article['content']

global_words=toker.tokenize(global_text)
global_words_stemmed=[stemmer.stem(word) for word in global_words]
global_words_stemmed_count=Counter(global_words_stemmed)
global_tokens=nltk.word_tokenize(global_text)
global_tokens_stemmed=[stemmer.stem(token) for token in global_tokens]
global_tokens_stemmed_count=Counter(global_tokens_stemmed)
global_sentences = sentence_splitter.tokenize(global_text)
global_najpogostejse_besede=global_words_stemmed_count.most_common(50)

#print(global_words)
#print(len(global_words))

file_dataset = open('dataset.tab', 'w+')
##### TVORBA ATRIBUTOV #####
toc()
print("***Zacetek tvorbe atributov")
tic()
interesting_characters=['.',',','?',':',';',' ','!','-','_','(','\"','/'] #<----- DODAJAJ


sestaviHeader=True
header=""
for article in articles:
    values=articles[article]
    number_words = sum(values['words'].values())
    number_spaces = values['content'].count(' ')
    number_tokens_withSpaces=sum(values['tokens'].values())+number_spaces #JE KOREKTNO DA PRISTEJEM PRESLEDKE? -> smem potem deliti s tem stevilom
    number_sentences = len(values['sentences'])
    record=""

    #IME DATOTEKE (PK)
    if sestaviHeader:
        header+='article name\t'
    record+=article+'\t'

    #AVTOR (Target Class 2)
    if sestaviHeader:
        header+='author\t'
    record+=values['author']+'\t'

    #SPOL AVTORJA (Target Class 2)
    if sestaviHeader:
        header += 'author gender\t'
    record += authors[values['author']]['gender'] + '\t'

    #FREKVENCE ZANIMIVIH ZNAKOV ZNOTRAJ BESEDILA
    for c in interesting_characters:
        if sestaviHeader:
            header+="% \'"+c.replace("\n", "\\n").replace("\t", "\\t")+"\'\t"
        if c in values['tokens']:
            record+=str(values['tokens'][c] / number_tokens_withSpaces )+'\t'
        else:
            record+="0\t"

    #RAZMERJE MED STEVILOM STAVKOV IN STEVILOM BESED ZNOTRAJ BESEDILA
    if sestaviHeader:
        header+='sentences-to-words ratio\t'
    record+=str(number_sentences / number_words)+'\t'

    #POVPRECNO STEVILO BESED V STAVKU ZNOTRAJ BESEDILA
    if sestaviHeader:
        header+='avg. sentence length\t'
    nChars = 0
    for s in values['sentences']:
        nChars += len(s)
    record += str(nChars / number_sentences)+'\t'

    #FREKVENCE GLOBALNO NAJPOGOSTEJSIH BESED V BESEDILU
<<<<<<< HEAD
    for word in global_najpogostejse_besede:
=======
    najpogostejse_besede=global_words_stemmed_count.most_common(100) #premakni iz zanke za pohitritev?
    for word in najpogostejse_besede:
>>>>>>> 4e2448ebede6d72980dbcb72eaab2584d1541f96
        if sestaviHeader:
            header+='%\"'+word[0].replace("\n", "\\n").replace("\t", "\\t")+'\"\t'
        if word[0] in values['words'].elements():
            record+=str(values['words'][word[0]] / number_words)+'\t'
        else:
            record+="0\t"




    ##### IZPIS V DATOTEKO #####
    if sestaviHeader:
        header=header[:-1]+'\n'
        file_dataset.write(header)
        sestaviHeader=False
    record=record[:-1]+'\n'
    file_dataset.write(record)
file_dataset.close()
toc()


##### VIZUALIZACIJA #####

#Stolpicni diagram najpogostejsih besed  in njihovih frekvenc v corpusu
#labels, values = zip(*global_najpogostejse_besede.items())
#indexes = np.arange(len(labels))
#width = 1
#plt.bar(indexes, values, width)
#plt.xticks(indexes + width * 0.5, labels)
#plt.show()
