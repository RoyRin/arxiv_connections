#/usr/bin/env python3
import arxiv
import pandas as pd
import queue
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# TODO : test discovery BFS Traversal

def discovery_BFS_traversal(root, max_depth, next_traversal_f):
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
    depth = 0
    timeToDepthIncrease = 1
    
    while not Q.empty() and depth <= max_depth:
        v = Q.get() 
        timeToDepthIncrease -= 1  

        print("another")
        adjacent_vs = next_traversal_f(v)
        print("-")
        for w in adjacent_vs:
            if w not in discovered:
                Q.put(w)
                discovered.add(w)
        
        if timeToDepthIncrease == 0:
            print("increase depths to ", depth+1)
            depth+=1
            timeToDepthIncrease = Q.qsize()

def search(search_query, max_search_results = 10000):
    print(f"searching : {search_query}")
    df= pd.DataFrame(arxiv.query(search_query, max_results = max_search_results))
    return df


def BFS_author_query(original_author, max_search_results = 10, max_depth = 5):
    """ Traverse the papers by coauthors and return a list of all the articles """

    def next_traversal_vertices(author, all_articles): 
        """ 
        return list of things to bump onto the queue, to traversal 1 deeper level
        also also update all_articles while on the way 
        HACK - all_articles is a list around a dataframe, to be able to pass by reference
            all_articles = [df.DataFrame], this allows one to update it
        """  
        # get arxiv articles for a specific search     
        arxiv_articles = search(author, max_search_results =max_search_results)
        # return True if author is a coauthor of article
        is_coauthor = lambda row : author in row.authors
        # get df of coauthored articles
        coauthored_articles = arxiv_articles[ arxiv_articles.apply(is_coauthor, axis = 1)]
        
        # update the master list of articles
        all_articles[0] = all_articles[0].append(coauthored_articles, ignore_index = True)
        
        # get a list of all the coauthors 
        unique_coauthors = set()
        for author_list in coauthored_articles.authors:
            for author in author_list:
                unique_coauthors.add(author) 
        
        return unique_coauthors
    
    # partially apply next_traversal_verticies to only take author as an arg, but to update the all_articles
    all_articles = [pd.DataFrame()]
    next_traversal_vertices_partially_applied = lambda author : next_traversal_vertices(author, all_articles) 
    
    discovery_BFS_traversal(original_author, max_depth= max_depth, next_traversal_f = next_traversal_vertices_partially_applied)
    return all_articles[0]

def get_authors_to_articles(all_articles):
    """ 
    input : dataframe of all articles
    returns : dict of author_name to article ids
    """
    author_to_articles = defaultdict(lambda:list)
    for i, row in all_articles.iterrows():
        for author in row.authors:
            author_to_articles[author].append(row.article)
    return author_to_articles

def create_edge(author1, author2, G):
    if G.has_edge(author1, author2):
        G[author1][author2]['weight']+=1
    else:
        G.add_edge(author1, author2, weight= 1)

def generate_author_graph(all_articles):
    """ return networkx graph of all the authors, with weights between them based on their shared papers"""
    G = nx.Graph()
    for i, row in all_articles.iterrows():
        for i in range(len(row.authors)):
            for j in range(i+1, len(row.authors)):
                create_edge(row.authors[i], row.authors[j], G)
    return G

def plot_weighted_graph(G):
    """Plot a weighted graph"""

    pos=nx.spring_layout(G) 
    nx.draw_networkx_nodes(G,pos,node_color='green')#,node_size=700)
    
    all_weights_sum = sum([G[e[0]][e[1]]['weight'] for e in G.edges])
    nx.draw_networkx_labels(G, pos=pos)
    # this seems wrong, but for now - individually plot each edge 
    for edge in G.edges:
        weight = G[edge[0]][edge[1]]['weight']
        width = weight*len(G.nodes)*10.0/all_weights_sum
        nx.draw_networkx_edges(G,pos,edgelist=[edge],width=width)
 
    plt.show() 


# example for weighted graph drawing: https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
if __name__ == "__main__":
    articles = BFS_author_query(original_author = "Alexandra Chouldechova", max_search_results= 5, max_depth= 2)

    # generate a graph of authors, where the weight is the number of papers shared
    G = generate_author_graph(articles)
    #plot_weighted_graph(G)
    if True:
        pos = nx.spring_layout(G)  # positions for all nodes
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()
    print(len(articles))
    
    
    #authors = author_search.authors
    # step 1 
    # get all the arxiv articles (for a given authorname)
    # compile a list of coauthors
    #   for each coauthor, 
    #       get a list of arxiv articles 
    #       compile a list of coauthor' 
    #   

# Relevant Plotly code for making graphs:
# https://plotly.com/python/network-graphs/

def BFS_author_query(original_author):
    """ BFS Traverse the papers to track the authors"""
    authors = queue.Queue()
    discovered = set()
    discovered.add(original_author)
    authors.put(original_author)
    while not authors.empty() and depth <= max_depth:
        author = authors.get()
        if author in discovered:
            continue

        arxiv_articles = search(author)
        unique_coauthors = get_unique_coauthors(arxiv_articles.authors)
        for author in unique_coauthors:
            if author not in discovered:
                authors.put(author)
                discovered.add(author)

##
def get_unique_coauthors(author, authors_lists):
    """
    Given a pandas series of lists of authors, 
    return a set of unique co-authors 
    """
    unique_authors = set()
    # Only consider authors that are directly co-authors with the original author
    relevant_lists = [author_list for author_list in authors_lists if author in author_list]
    
    coauthored_articles = [article for article in arxiv_articles if author in article['authors']]
    for authors in coauthored_articles['authors']:
        for author in authors:
            unique_authors.add(author)
    return unique_authors