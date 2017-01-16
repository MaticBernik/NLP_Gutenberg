import os
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import wordnet
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
#nltk.download() #<- ODKOMENTIRAJ CE POGANJAS PRVIC!

projectDir = "/home/matic/Dropbox/Inteligentni Sistemi/Assigment2/"
os.chdir(projectDir)
#Atributi izpeljani iz stevila pojavitev znakov znotraj dokumenta so pretvorjeni v frekvence znotraj istega dokumenta
#---> nacin normalizacije zaradi neenakomerne dolzine clankov



#Predpriprave na procesiranje texta
stemmer = nltk.stem.PorterStemmer()
punkt_param = PunktParameters()
sentence_splitter = PunktSentenceTokenizer(punkt_param)
toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)

articles={}
print("***Zacetek obdelave clankov")
##### OBDELAVA CLANKOV #####
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

print("***Zacetek Globalne obdelave")
##### GLOBALNA OBDELAVA CLANKOV #####
#Proceseranje clankov na globalni ravni
#boljsi pristop sestevanja slovarjev vseh clankov  ali  sesteti vse clanke v en string in ga loceno sprocesirati?? --> stopaj?
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
global_tokens=nltk.word_tokenize(text)
global_tokens_stemmed=[stemmer.stem(token) for token in global_tokens]
global_tokens_stemmed_count=Counter(global_tokens_stemmed)
global_sentences = sentence_splitter.tokenize(global_text)

#print(global_words)
#print(len(global_words))

file_dataset = open('dataset.tab', 'w+')


##### TVORBA ATRIBUTOV #####
print("***Zacetek tvorbe atributov")
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

    #AVTOR (Target Class)
    if sestaviHeader:
        header+='author\t'
    record+=values['author']

    #FREKVENCE ZANIMIVIH ZNAKOV ZNOTRAJ BESEDILA
    for c in interesting_characters:
        if sestaviHeader:
            header+="% \'"+c+"\'\t"
        if c in values['tokens']:
            record+=str(values['tokens'][c] / number_tokens_withSpaces )+'\t'
        else:
            record+="0\t"

    #RAZMERJE MED STEVILOM STAVKOV IN STEVILOM BESED ZNOTRAJ BESEDILA
    if sestaviHeader:
        header+='sentences-to-words ratio'
    record+=str(number_sentences / number_words)+'\t'

    #POVPRECNO STEVILO BESED V STAVKU ZNOTRAJ BESEDILA
    if sestaviHeader:
        header+='avg. sentence length'
    nChars = 0
    for s in values['sentences']:
        nChars += len(s)
    record += str(nChars / number_sentences)+'\t'

    #FREKVENCE GLOBALNO NAJPOGOSTEJSIH BESED V BESEDILU
    najpogostejse_besede=global_words_stemmed_count.most_common(50) #premakni iz zank za pohitritev?
    for word in najpogostejse_besede:
        if sestaviHeader:
            header+='%\"'+word[0]+'\"\t'
        if word in values['words']:
            record+=str(values['words'][word][1])+'\t'
        else:
            record+="0\t"




    ##### IZPIS V DATOTEKO #####
    if sestaviHeader:
        header=header[:-1]+'\n'
        file_dataset.write(header)
        sestaviHeader=False
    record=record[:-1]+'\n'
file_dataset.close()

