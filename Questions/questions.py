import nltk
import sys
import os
#from nltk import word_tokenize
#nltk.download('stopwords')
import math
import numpy
import string




FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)
    #print('                 idf      :',idfs["connect"])


    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    filedict=dict()
    arr=os.listdir(directory)
    print('arr=',arr)

    os.chdir(directory)
    i=0
    for filename in arr:
        i+=1
        content=open(filename,'r',encoding='utf-8').read()
        filedict[filename]=content
        
    return filedict

      
   
    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    wtr=[]
    
    lowerdoc=document.lower()
    wordlist=nltk.word_tokenize(lowerdoc)
    for word in wordlist:
        if word in string.punctuation:
            wtr.append(word)
        elif word in nltk.corpus.stopwords.words("english"):
            wtr.append(word)

    

    for a in wtr:
        wordlist.remove(a)

    
    
    #print(wordlist)
    return wordlist

    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.


WHEN USING DOCS.VALUES()
              
            for word in sentence:
                print(word)
            
                
                #USE COUNT FROM MATH LIB U
                wcount=sentence.count(word)
                total=wcount
                if word not in result.keys():
                    result[word]=total
                #print('word=',word,'count:', wcount)
        
            

    """

    df={}
    result={}
    i=0
    for filename in documents.keys():
        i+=1

        file=documents[filename]
        for word in file:
            try:
                df[word].add(i)
            except:
                df[word] = {i}

    for key in df.keys():
        value=df[key]
        num=len(value)
        idf=len(documents)/num
        final=numpy.log(idf)
        result[key]=final

    return result









   
    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
        print(query)
    final=dict()

        
    result=dict()
    for filename in files.keys():
         result[filename]=0
    for word in query:
        for filename in files.keys():
            wordlist=files[filename]
                
            wcount=wordlist.count(word)
            idf=idfs[word]
            prod=idf*wcount
            print(word,'  ', wcount, ' ', idf, ' ', prod)
            result[filename]+=prod
  


    """
    print(query)
    final=dict()

        
    result=dict()
    for filename in files.keys():
         result[filename]=0
    for word in query:
        for filename in files.keys():
            wordlist=files[filename]
                
            wcount=wordlist.count(word)
            idf=idfs[word]
            prod=idf*wcount
            print(word,'  ', wcount, ' ', idf, ' ', prod)
            result[filename]+=prod
  


        
    sort = sorted(result.items(), key=lambda x: x[1], reverse=True)
    #print(sort)
    finallist=[]
   
    d=0
    for elem in sort:
        d+=1

        finallist.append(elem[0])
        

        if d==n:
            break

    return finallist
            
    
            
            
    #raise NotImplementedError

def qtd(query,wlist):
    i=0
    for word1 in query:
        for word2 in wlist:
            
            if word1==word2:
                i+=1
    length=len(wlist)
    num=i/length
    

    return num


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    ""
        for sentence in sentences.keys():
        result[sentence]=0
    for word in query:
        for sentence in sentences.keys():
            value=[0,0]
            wordlist=sentences[sentence]

            if word in wordlist:
                value[0]+=idfs[word]

            number=qtd(query,wordlist)
            value[1]+=number

            result[sentence]=value 
     result=dict()
    for sentence in sentences.keys():
        result[sentence]=0

    for sentence in sentences.keys():
        wordlist=sentences[sentence]
        value=[0,0]
        for word in query:
            if word in wordlist:
                value[0]+=idfs[word]

        number=qtd(query,wordlist)
        value[1]+=number

        result[sentence]=value
    """
    print(query)
    result=dict()
    for sentence in sentences.keys():
        result[sentence]=0
    for sentence in sentences.keys():
        wordlist=sentences[sentence]
        value=[0,0]
        for word in query:
            if word in wordlist:
                value[0]+=idfs[word]
                #print('yes',word,value)

        number=qtd(query,wordlist)
        value[1]+=number

        result[sentence]=value
        
   

    sort = sorted(result.items(), key=lambda x: (x[1][0],x[1][1]), reverse=True)
    for i in range(10):
        print(sort[i])
    finallist=[]
    d=0  
    
    for elem in sort:
        d+=1

        finallist.append(elem[0])
        #print(d,finallist)

        if d==n:
            break

    return finallist
            


    
    #raise NotImplementedError


        

if __name__ == "__main__":
    main()
