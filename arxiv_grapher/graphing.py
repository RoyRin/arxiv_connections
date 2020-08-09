import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
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
    plt.show()


    

# example for weighted graph drawing: https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html

# TODO : color the original author
# TODO : put the original author in the center of the plot
# TODO : explore plotly

# plotly
# https://plotly.com/python/network-graphs/


def plot_plotly_simple(G, original_name = None):
    """
    https://plotly.com/python/plotly-fundamentals/    
    
    more relevant taken from : https://stackoverflow.com/questions/51410283/how-to-efficiently-create-interactive-directed-network-graphs-with-arrows-on-p

    """
    pos = nx.spring_layout(G)
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    # Make list of nodes for plotly
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Make a list of edges for plotly
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

        
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    ''' Color nodes'''
    node_adjacencies = []
    node_text = []
    for _, adjacencies in enumerate(G.adjacency()):
        name, connections = adjacencies
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f"{name} : #{len(connections)} connections")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Arxiv co-author exploration tracker ',
                    titlefont_size=16,
                    showlegend=True,
                    #hovermode='closest',
                    #mode="lines+markers+text",
                    margin=dict(b=20,l=5,r=5,t=40),
                    
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.update_traces(textposition='top center')
    #fig.update_layout(height=800, title_text='GDP and Life Expectancy (Americas, 2007) )

    fig.show()



def graph(G, original_name = None):
    #plot_weighted_graph(G)
    plot_plotly(G, original_name)

    