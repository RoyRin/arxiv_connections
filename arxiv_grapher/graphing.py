import networkx as nx
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger()


def plot_weighted_graph(G):
    """Plot a weighted graph"""

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='green')  #,node_size=700)

    all_weights_sum = sum([G[e[0]][e[1]]['weight'] for e in G.edges])
    nx.draw_networkx_labels(G, pos=pos)
    # this seems wrong, but for now - individually plot each edge
    for edge in G.edges:
        weight = G[edge[0]][edge[1]]['weight']
        width = weight * len(G.nodes) * 10.0 / all_weights_sum
        nx.draw_networkx_edges(G, pos, edgelist=[edge], width=width)

    plt.show()

def simple_plot(G):
    #pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, with_labels=True, font_weight='bold')


    

# example for weighted graph drawing: https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html

# TODO : color the original author
# TODO : put the original author in the center of the plot
# TODO : explore plotly

# plotly
# https://plotly.com/python/network-graphs/




def graph(G):
    plot_weighted_graph(G)
    plt.show()