import arxiv
import pandas as pd
import queue
from collections import defaultdict
import networkx as nx
import logging
import ast

logger = logging.getLogger()

# TODO : traverse people, but then in the final plot, only show people maximally X distance away (prune graph by distance)
# TODO - be able to create a report on a person, based on their 'proximity' to another academic


def discovery_BFS_traversal(root, max_depth, next_traversal_f, max_queries= None):
    """
    Traverse from a root BFS, 
    apply next_traversal_f to get the next set of vertices
    :param root: 
    :param max_depth: [int] - max depth to traverse graph using BFS
    :param next_traversal_f: function(obj) - returns a list of objects to add to the queue 
    """
    Q = queue.Queue()
    discovered = set()

    discovered.add(root)
    Q.put(root)
    depth = 1
    timeToDepthIncrease = 1
    query_count =0
    while not Q.empty() and depth <= max_depth:
        query_count+=1
        if max_queries is not None and query_count > max_queries:
            break
        v = Q.get()
        timeToDepthIncrease -= 1
        adjacent_vs = next_traversal_f(v, depth)
        for w in adjacent_vs:
            if w not in discovered:
                Q.put(w)
                discovered.add(w)

        if timeToDepthIncrease == 0:
            depth += 1
            logger.debug(f"increase depth to {depth}")
            timeToDepthIncrease = Q.qsize()


def search(author, ignore_high_author_count = None, max_search_results=100):
    logging.debug(f"searching : {author}")
    auth = author.replace("-", "_")
    splits = auth.split(" ")
    if len(splits) ==2:
        auth = f"{splits[1]}_{splits[0]}"
    else:
        auth = splits[-1]

    query = f"au:{auth}"
    results = arxiv.Search(query, max_results=max_search_results).results()
    #df = pd.DataFrame(arxiv.query(search_query,
    #                              max_results=max_search_results))
    ret =[]
    for paper in results:
        if ignore_high_author_count is not None:
            if len(paper.authors) > ignore_high_author_count:
                continue
        paper_authors = [author.name for author in paper.authors]
        ret.append({"authors": paper_authors, "title": paper.title, "url": paper.pdf_url})
    df = pd.DataFrame(ret)
    return df


def BFS_author_query(original_author,
                     max_search_results=10,
                     halve_queries_by_depth=True,
                     ignore_high_author_count=20,
                     max_depth=5, max_queries = 30
                     ):
    """ Traverse the papers by coauthors and return a list of all the articles """
    original_author = original_author.lower()
    query_count = 0
    def next_traversal_vertices(author, depth, all_articles):
        """ 
        return list of things to bump onto the queue, to traversal 1 deeper level
        also also update all_articles while on the way 
        HACK - all_articles is a list around a dataframe, to be able to pass by reference
            all_articles = [df.DataFrame], this allows one to update it
        """
        # get arxiv articles for a specific search
        
        max_results_ = int(max_search_results * (1 / 2)**(depth - 1)) if halve_queries_by_depth else max_search_results 
        
        arxiv_articles = search(author,ignore_high_author_count=ignore_high_author_count, max_search_results=max_results_)

        
        #if ignore_many_author_paper:
            #arxiv_articles = arxiv_articles[arxiv_articles.authors.apply(

        # return True if author is a coauthor of article
        is_coauthor = lambda row: any([
            author.lower() == article_author.lower()
            for article_author in row.authors
        ])
        # get df of coauthored articles
        coauthored_articles = arxiv_articles[arxiv_articles.apply(is_coauthor,
                                                                  axis=1)]

        # update the master list of articles
        all_articles[0] = pd.concat([all_articles[0], coauthored_articles])

        # get a list of all the coauthors
        unique_coauthors = set()
        if not len(coauthored_articles):
            return []
        for author_list in coauthored_articles.authors:
            for author in author_list:
                unique_coauthors.add(author.lower())

        return unique_coauthors

    # partially apply next_traversal_verticies to only take author as an arg, but to update the all_articles
    all_articles = [pd.DataFrame()]
    next_traversal_vertices_partially_applied = lambda author, depth: next_traversal_vertices(
        author, depth, all_articles)

    discovery_BFS_traversal(
        original_author,
        max_depth=max_depth,
        next_traversal_f=next_traversal_vertices_partially_applied,
        max_queries=max_queries)
    return all_articles[0]


def get_authors_to_articles(all_articles):
    """ 
    helper function # TODO - currently this function isn't used
    input : dataframe of all articles
    returns : dict of author_name to article ids
    """
    author_to_articles = defaultdict(lambda: list)
    for _, row in all_articles.iterrows():
        for author in row.authors:
            author_to_articles[author].append(row.article)
    return author_to_articles


# TODO - see if there is a differnet way to do this - is this accidentally directed?
def _create_edge(author1, author2, G):
    """ helper function that """
    if G.has_edge(author1, author2):
        G[author1][author2]['weight'] += 1
    else:
        G.add_edge(author1, author2, weight=1)


# TODO - take max-depth in generate-author-graph (so this is isn't only configurable in generating the articles data)
def generate_author_graph(all_articles):
    """ return networkx graph of all the authors, with weights between them based on their shared papers"""
    G = nx.Graph()
    for authors in all_articles.authors:
        # Lists are sometimes read into a string, convert it back to a list of authors
        # (i.e. "['asda', 'bb' ]" -> ['asda', 'bb'])
        if isinstance(authors, str):
            authors = ast.literal_eval(authors)

        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                _create_edge(authors[i].lower(), authors[j].lower(), G)
    return G
