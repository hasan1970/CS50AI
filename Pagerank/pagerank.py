import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    dict1={}
    a=corpus[page]
    i=len(a)
    if i!=0:
        for link in corpus:
            dict1[link]= (1-damping_factor)/len(corpus)
        for link in a:
            dict1[link]= (damping_factor)/i
    else:
        for link in corpus: 
            dict1[link]=1/len(corpus)

    return dict1
        
    
    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    dict2={}
    for key in corpus:
        dict2[key]=0
    randpage=random.choice(list(corpus.keys()))
    dict2[randpage]+=1/n
    

    
    for j in range(1,n):
        transmodel=transition_model(corpus, randpage, damping_factor)
        nextpages=[]
        prob=[]
        nextpages.extend(transmodel.keys())
        prob.extend(transmodel.values())

        randpage= random.choices(nextpages, weights=prob)[0]
        dict2[randpage]+=1/n
        
    return dict2



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    dict3=dict()    

    d=damping_factor
    N=len(corpus)
    for key in corpus:
        dict3[key]=1/N #in the beginning, all have equal probablities        

    limit=0.001 

    dict4= copy.deepcopy(dict3) 
    
    count=0 #to avoid reference before assignment error
    while count<N: 
        count=0 #resetting the value
        for key in corpus:
            first=(1-d)/N
            second=0
            for link in corpus:
                if key in corpus[link]:
                    numlinks=len(corpus[link])
                    second+=dict3[link]/numlinks 
            second= d*second
            total=first+second

            if abs(dict3[key] - total) < limit:
                count += 1
                
            dict4[key]=total
        dict3 = copy.deepcopy(dict4)       
    
    return dict4

if __name__ == "__main__":
    main()
