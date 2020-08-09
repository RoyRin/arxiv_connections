import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import logging

logger = logging.getLogger()

# TODO - for each hover, show the distance to the original author


def plot_weighted_graph(G):
    """Plot a weighted graph"""

    pos = nx.spring_layout(G, weight="weight")
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

# plotly
# https://plotly.com/python/network-graphs/


def _make_edge(x, y, width):  # TODO - this isn't used yet
    """
    Args:
        x: a tuple of the x from and to, in the form: tuple([x0, x1, None])
        y: a tuple of the y from and to, in the form: tuple([y0, y1, None])
        width: The width of the line

    Returns:
        a Scatter plot which represents a line between the two points given. 
    """
    return go.Scatter(x=x,
                      y=y,
                      line=dict(width=width, color='#888'),
                      hoverinfo='none',
                      mode='lines')


# TODO - would be nice if I could see topics, or get a link to the person webpage when I click on them
# TODO - add hover text over edges
# note: this ^ might not be possible :( https://stackoverflow.com/questions/55962964/adding-hover-text-to-plotly-scatter-plot-lines-or-multiple-colors-for-scatter-pl
# TODO - add width to the edges by weight
# TODO - consider using Dash to visualize a whole dashboard of people interactively
#   for ^ check this : https://www.youtube.com/watch?v=hSPmj7mK6ng


def plot_plotly_simple(G, original_name=None):
    """
    Generate networkx plot using Plotly
        Note : Plotly doesn't have a direct way to plot a networkx Graph
        So, we scatter plot points, and draw lines between them  
    https://plotly.com/python/plotly-fundamentals/    
        Here is a description of plotly figures: https://plotly.com/python/figure-structure/ 
    more relevant taken from : https://stackoverflow.com/questions/51410283/how-to-efficiently-create-interactive-directed-network-graphs-with-arrows-on-p

    """
    original_name = original_name.lower()
    # compute shortest path to get to original node (unweighted distance)
    shortest_path = dict(nx.all_pairs_shortest_path_length(G))

    pos = nx.spring_layout(G, weight="weight")
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
    edge_text = []
    for edge in G.edges():
        n1 = edge[0]
        n2 = edge[1]
        x0, y0 = G.nodes[n1]['pos']
        x1, y1 = G.nodes[n2]['pos']
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        d = G.get_edge_data(n1, n2)
        # TODO - currently edge weights do not visualize. NEED TO FIX
        weight_text = d.get("weight", "N/A")
        edge_text.append(f"shared papers: {weight_text}")

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        mode="lines",
        #mode="markers+text",
        hoverinfo='text')
    edge_trace.text = edge_text
    node_trace = go.Scatter(x=node_x,
                            y=node_y,
                            mode="markers",
                            hoverinfo='text',
                            marker=dict(showscale=True,
                                        colorscale='YlGnBu',
                                        reversescale=True,
                                        color=[],
                                        size=10,
                                        colorbar=dict(thickness=15,
                                                      title='Node Connections',
                                                      xanchor='left',
                                                      titleside='right'),
                                        line_width=2))
    # Plot the original node as red, to make it easier to see
    node_trace_original = None
    if original_name and original_name in G.nodes:
        original_x, original_y = G.nodes[original_name]['pos']
        node_trace_original = go.Scatter(x=[original_x],
                                         y=[original_y],
                                         mode="markers+text",
                                         hoverinfo='text',
                                         marker=dict(color=["Red"],
                                                     size=9,
                                                     line_width=2))

    #Color nodes and add hover-text
    node_adjacencies = []
    node_text = []
    for _, adjacencies in enumerate(G.adjacency()):
        name, connections = adjacencies
        node_adjacencies.append(len(adjacencies[1]))
        hover_text = name
        if original_name and original_name in G.nodes:
            dist = shortest_path[original_name][name]
            hover_text += (f"<br>dist-to-origin : {dist}")

        hover_text += f"<br>Papers pulled: {len(connections)}"
        #neighbors = list(G.neighbors(name))
        # TODO - sort the co-authors by number of papers shared
        coauthors = sorted(G[name].items(),
                           key=lambda edge: edge[1]['weight'],
                           reverse=True)

        if coauthors:
            hover_text += f"<br>co-authors:"
        for coauthor, weight_dict in coauthors:

            hover_text += "<br>" + str(coauthor) + " : " + str(
                weight_dict.get('weight', "N/A"))
        node_text.append(hover_text)

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    # Plot the nodes and edges, and if original name supplied, highlight the original name
    data = [edge_trace, node_trace]
    if node_trace_original:
        data.append(node_trace_original)
    fig = go.Figure(data=data,
                    layout=go.Layout(
                        title='<br>Arxiv co-author exploration tracker ',
                        titlefont_size=16,
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False,
                                   zeroline=False,
                                   showticklabels=False),
                        yaxis=dict(showgrid=False,
                                   zeroline=False,
                                   showticklabels=False)))
    fig.show()


def graph(G, original_name=None):
    #plot_weighted_graph(G)
    plot_plotly_simple(G, original_name)
