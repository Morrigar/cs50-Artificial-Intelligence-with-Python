import os
import random
import re
import sys

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
    ans = {}
    if len (corpus[page])==0:
        ans = {key:1/len(corpus) for key in corpus.keys()}
        return ans
    for key in corpus.keys():
        randomProb = (1 - damping_factor)/len(corpus)
        choiceProb = damping_factor/len(corpus[page])
        if key in corpus[page]:
            ans [key] = randomProb + choiceProb
        else:
            ans [key] = randomProb
    return ans


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ans = {}
    for key in corpus.keys():
        ans [key] = 0
    startPage = random.choice([key for key in corpus.keys()])
    transModel = transition_model(corpus, startPage, damping_factor)
    ans [startPage] += 1
    for i in range (n):
        choices = [key for key in transModel.keys()]
        weights = [weight for weight in transModel.values()]
        choice = random.choices(choices, weights)[0]
        ans [choice] += 1
        transModel = transition_model(corpus, choice, damping_factor)
    total = sum(ans.values())
    for key in ans.keys():
        ans [key] = ans[key]/total
    return ans


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ans = {key:1/len(corpus) for key in corpus.keys()}  # Create answer dictionary.  ALl pageranks to 1/number of pages.
    randChance = (1-damping_factor)/len(corpus)         # Calculate the chance of randomly landing on the page.
    stopCalc = False                                    # stopCalc is a flag for determining when to stop iterating.
    while not stopCalc:
        newAns = {key: ans[key] for key in ans}
        for page in corpus:
            referrers = [key for key in corpus.keys() if page in corpus [key]]  # Make a list of referring pages.
            sumPRi = 0
            for rpage in referrers:                                             # Calculate Sum PRi for all
                PRi = ans[rpage]                                                # referring pages.
                numLinks = len(corpus[rpage])
                sumPRi += PRi/numLinks
            newAns[page] = randChance + damping_factor * sumPRi
        for key in ans.keys():
            if abs(ans[key]-newAns[key]) < 0.001:
                stopCalc = True
            else:
                stopCalc = False
        ans = {key: newAns[key] for key in ans}             # Adjust the iterated values before reiterating.
    totalProb = sum (value for value in ans.values())       # Ensure the values are expressed as probabilities.
    ans = {key:ans[key]/totalProb for key in ans}           # Set new answers to recalculated values.

    return ans

if __name__ == "__main__":
    main()
