import os
import nltk
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import wordnet
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer

#nltk.download()

projectDir = "/home/matic/Dropbox/Inteligentni Sistemi/Assigment2/"
os.chdir(projectDir)
file_dataset = open('dataset.tab','w+')
#Atributi izpeljani iz stevila pojavitev znakov znotraj dokumenta so pretvorjeni v frekvence znotraj istega dokumenta
#---> nacin normalizacije zaradi neenakomerne dolzine clankov
header=('article name\tauthor\t%periods\t%commas\t%question marks\t%colons\t%semi-colons\t%blanks\t%exclamation marks\t%dashes\t%underscores\t%brackets\t%quotations\t%slashes\t%sentences\tavg. sentence length')
records=""
interesting_characters=['.',',','?',':',';',' ','!','-','_','(','\"','/']
#Pripravi 'stemmer' za kasnejse iskanje korenov besed
stemmer = nltk.stem.PorterStemmer()
#Priprava za deljenje texta na stavke
punkt_param = PunktParameters()
sentence_splitter = PunktSentenceTokenizer(punkt_param)
#Priprava za deljenje texta na besede
toker = RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
for author in os.listdir("articles/"): #iterate trough authors
    if os.path.isdir(projectDir+'articles/'+author):
        for article in os.listdir('articles/'+author):
            with open('articles/'+author+'/'+article,'r') as file:
                text = file.read()
                text_lowerCase = text.lower() #text to lower case
            tokens_noPunctuations = toker.tokenize(text)
            stems_noPunctuations = [stemmer.stem(word) for word in tokens_noPunctuations]
            stem_noPunctuations_count = Counter(stems_noPunctuations)
            tokens = nltk.word_tokenize(text_lowerCase) #tokenize text
            stems = [stemmer.stem(word) for word in tokens]
            stem_count = Counter(stems)
            record=article+'\t'+author+'\t'
            number_words = sum(stem_noPunctuations_count.values())
            ##### ATRIBUTI: FREKVENCE ZNAKOV V CLANKU #####
            #vsi so normalizerani glede na stevilo tokenov v clanku
            number_spaces=text.count(' ')
            number_tokens=sum(stem_count.values())+number_spaces
            for c in interesting_characters:
                if c==' ':
                    record+=str(number_spaces/number_tokens)+'\t'
                elif c in stem_count:
                    record+=str(stem_count[c]/number_tokens)+'\t'
                else:
                    record+='0\t'
            ##### ATRIBUTI: RAZMERJA GLEDE NA STEVILO STAVKOV #####
            #normalizeran glede na stevilo besed v clanku
            sentences = sentence_splitter.tokenize(text)
            number_sentences = len(sentences)
            #rezmerje med stevilom stavkov in stevilom besed v clanku
            record+=str(number_sentences/number_words)+'\t'
            #povprecno stevilo znakov v stavku
            nChars=0
            for s in sentences:
                nChars+=len(s)
            record+=str(nChars/len(sentences))+'\t'

            ##### DODAJ VRSTICO V TABELO #####
            record = record[:-1] + '\n'
            records+=record

##### ZAPIS V DATOTEKO #####
header+='\n'
file_dataset.write(header)
#print(record)
file_dataset.write(records)




#corpus = PlaintextCorpusReader("articles", '.*')
#syns = wordnet.synsets('program') #get words with similar meaning

#stemmer = nltk.stem.PorterStemmer()
#documents_stems_count={} #file name : ([stem_list],#occurences)
#documents_stems={} #file_name: [stem_list]
#for file in corpus.fileids():
#    #tagged = nltk.pos_tag(corpus.words(file)) #oznaci besede glede na vlogo v stavku
#    words = corpus.words(file)
#    words_stemmed=[]
#    for word in words:
#        word=word.lower() #to lower case
#        words_stemmed.append(stemmer.stem(word))
#    stem_count = Counter(words_stemmed) #number of stem occurences in a file
#    #documents_stems_count[file]=stem_count
#    documents_stems[file]=words_stemmed
#    #print(documents_stems.most_common(100))

#tfidf = TfidfVectorizer()
#tfs = tfidf.fit_transform(documents_stems.values())
#print(tfs)
file_dataset.close()