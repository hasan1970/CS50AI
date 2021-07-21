import nltk
import sys
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | NP VP Adv | VP




NP -> N | P Det AP | P NP | NP NP | Det N | NP Adv
AP ->  Adj N | Det AP | AP NP | Adj AP | Adj 
VP -> V | V NP | V AP | Adv VP
"""
# in NP : 

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
 

        wtr=[] #words to remove

    #print("sentence b4:", sentence)
    lowersent=sentence.lower()
    #print("sentence after:", lowersent)
    wordlist=lowersent.split()
    #print('list of words : ',wordlist)
    for word in wordlist:
     #   print('word : ', word)
        for letter in word:
          #  print('letter : ',letter)

            if letter == '.':
                wordlist.remove(word)
                word=word[:-1]
                wordlist.append(word)
            elif letter not in 'abcdefghijklmnopqrstuvwxyz':
                if word in wtr:
                    continue
                wtr.append(word)

                
    for thing in wtr:
        wordlist.remove(thing)
    #print(wordlist)
    return wordlist  
  
    """
    lowersent=sentence.lower()
    wordlist=nltk.tokenize.word_tokenize(lowersent)
    for word in wordlist:
        if word=='.':
            wordlist.remove('.')

    
    
        
    return wordlist




   # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

                    

    """
    np=[]
    #print(tree)
    for sub in tree.subtrees():
        #print('sub=',sub)
        if sub.label()=='NP':
            #print('sub with NP=',sub)
            a=[]
            for sub2 in sub.subtrees():
                if sub==sub2:
                    continue
                
                #print('sub2=',sub2)
                a.append(sub2.label())
                if sub2.label()=='NP':                 
                 #   print('break')
                    break
                elif sub2.label() != 'N':
                #    print('continue')
                    continue

            else:
                
                if sub.label()=='NP':
                    if sub not in np:
                        #print('APPENDED')
                        np.append(sub)
                
                
               
                
                    
               
            
    #print('np=',np)
    return np
      
   # raise NotImplementedError


if __name__ == "__main__":
    main()
