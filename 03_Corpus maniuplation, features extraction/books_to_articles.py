import os
projectDir = "/home/matic/Dropbox/Inteligentni Sistemi/Assigment2/"
os.chdir(projectDir)

for filename in os.listdir("books/"):
        if filename.endswith(".txt"):
            book = open("books/"+filename,"r")
            for i in range(2000): #because we don't want to work with book content before actual start of story - skip first 2000 lines
                next(book)
            for line in book: # we skip lines until we reach next paragraph
                if line=='\n':
                    break

            num_articles = 30;
            minLength_article=500; #Minimum number of words in each article
            filename_noSuffix=filename[:-4]
            for i in range(num_articles):
                length_article=0
                content_article=''
                while length_article < minLength_article:
                    for line in book: #add next paragraph to book
                        if line=='\n':
                            break
                        else:
                            content_article+=line

                    length_article=len(content_article.split()) #check article length
                filename_output="articles/"+filename_noSuffix+"_"+str(i)+".txt"
                output = open(filename_output,"w")
                output.write(content_article)
                output.close()
            book.close()
