import os
projectDir = "/home/matic/Dropbox/Inteligentni Sistemi/Assigment2/"
os.chdir(projectDir)
for author_dir in os.listdir("books/"): #iterate trough authors
    if not os.path.exists("articles/"+author_dir):
        os.makedirs("articles/"+author_dir)
    books_dir = "books/" + author_dir + "/txt/"
    headers_dir = "books/" + author_dir + "/header/"
    for filename in os.listdir(books_dir): #iterate trough books
        if os.path.getsize(books_dir+filename) < 105000: #if book too short -> skip it
            continue
        if filename.endswith(".txt"):
            book = open(books_dir+filename,"r",encoding="latin-1")
            for i in range(400): #because we don't want to work with book content before actual start of story - skip first 2000 lines
                next(book)
            for line in book: # we skip lines until we reach next paragraph
                if line=='\n':
                    break

            num_articles = 20;
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
                filename_output="articles/"+author_dir+"/"+filename_noSuffix+"_"+str(i)+".txt"
                #filename_output = "articles/" + filename_noSuffix + "_" + str(i) + ".txt"
                #copy header file also??
                output = open(filename_output,"w")
                output.write(content_article)
                output.close()
            book.close()
