import os
import random
import re
import copy
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
    probability_distribution = dict()
    pages_in_corpus = len(corpus)
    links_in_current_page = len(corpus[page])
    for random_page in corpus:
        if links_in_current_page == 0:
            probability_distribution[random_page] = (damping_factor / pages_in_corpus) + ((1 - damping_factor) / pages_in_corpus)
        else:
            if random_page in corpus[page]:
                probability_distribution[random_page] = (damping_factor / links_in_current_page) + ((1 - damping_factor) / pages_in_corpus)
            else:
                probability_distribution[random_page] = ((1 - damping_factor) / pages_in_corpus)
    return probability_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    page = None
    trans_model = None
    for _ in range(n):
        if not page:
            page = random.choice(list(corpus.keys()))
            page_ranks[page] = 1
        else:
            pages = list(trans_model.keys())
            probabilities = list(i * 100 for i in trans_model.values())
            page = random.choices(pages, weights=tuple(probabilities), k=1)[0]
            if page in page_ranks:
                page_ranks[page] += 1
            else:
                page_ranks[page] = 1
        trans_model = transition_model(corpus, page, damping_factor)
    for page, visits in page_ranks.items():
        page_ranks[page] = visits / n
    return page_ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = dict()
    n = len(corpus)
    d = damping_factor

    for page in corpus:
        page_ranks[page] = 1 / n

    converged = False
    while not converged:
        distribution = copy.deepcopy(page_ranks)
        for page in page_ranks:
            page_ranks[page] = (1 - d) / n + d * iterative_sum(page, distribution, corpus)
            if abs(distribution[page] - page_ranks[page]) < 0.001:
                converged = True
                
    return page_ranks

def iterative_sum(p, distribution, corpus):
    sum = 0
    for i in [page for page, links in list(corpus.items()) if p in links]:
        sum += distribution[i] / len(corpus[i])
    return sum

if __name__ == "__main__":
    main()
