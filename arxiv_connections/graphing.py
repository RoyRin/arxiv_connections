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
def add_plotly_hover_text(G, shortest_path, original_name):
    #Color nodes and add hover-text
    node_adjacencies = []
    node_text = []
    for _, adjacencies in enumerate(G.adjacency()):
        # adjacencies looks like : (name, {name: {weight:3}, ... } ... )
        name, connections = adjacencies

        node_adjacencies.append(len(connections))
        hover_text = name.upper()
        if original_name and original_name in G.nodes:
            dist = shortest_path[original_name][name]
            hover_text += (f"<br>Distance to origin : {dist}")
        hover_text += f"<br># connections: {len(connections)}"

        num_papers_connections = sum(
            [d["weight"] for d in connections.values()])
        hover_text += f"<br># papers connections: {num_papers_connections} (approx)"
        coauthors = sorted(G[name].items(),
                           key=lambda edge: edge[1]['weight'],
                           reverse=True)
        if coauthors:
            hover_text += f"<br>Co-Authors:"
        for coauthor, weight_dict in coauthors:
            hover_text += "<br> " + str(coauthor.title()) + " : " + str(
                weight_dict.get('weight', "N/A"))
        node_text.append(hover_text)
    return node_adjacencies, node_text


def add_plotly_edge_trace(G):
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
    return edge_trace


def add_plotly_node_trace(G, original_name):
    # Make list of nodes for plotly
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
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
    shortest_path = dict(nx.all_pairs_shortest_path_length(G))
    node_adjacencies, node_text = add_plotly_hover_text(
        G, shortest_path, original_name)
    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    return node_trace


def circular_layout_partially_fixed(G, original_name):
    """
    first layer outside of the original node is fixed on a circle, everything else is 
    force-directed
    """
    # TODO - currently this isn't used, address that!
    all_paths_shortest_path = dict(nx.all_pairs_shortest_path_length(G))
    sp_from_origin = all_paths_shortest_path[original_name]
    nodes_at_depth_1 = [node for node in G.nodes if sp_from_origin[node] == 1]
    circle_pos = nx.circular_layout(nodes_at_depth_1,
                                    scale=.1,
                                    center=[0., 0.])
    pos = nx.spring_layout(G,
                           pos=circle_pos,
                           fixed=nodes_at_depth_1,
                           weight="weight")
    return pos


def concentric_circles(G, original_name):
    """ each deeper layer of the graph is represented further out in the concentric ring"""
    all_paths_shortest_path = dict(nx.all_pairs_shortest_path_length(G))
    sp_from_origin = all_paths_shortest_path[original_name]
    pos = {}
    depth = 0
    positioned = 0
    scale = .1
    while positioned != len(G.nodes):
        nodes_at_depth = [
            node for node in G.nodes if sp_from_origin[node] == depth
        ]
        circle_pos = nx.circular_layout(nodes_at_depth,
                                        scale=scale,
                                        center=[0., 0.])
        pos = {**pos, **circle_pos}
        positioned += len(nodes_at_depth)
        depth += 1
        scale += 0.1

    return pos


def plot_plotly(G, original_name=None, concentric_circle_graphing=False):
    """
    concentric_circles is a boolean flag, for visualizing graph in concentric circles 

    Generate networkx plot using Plotly
        Note : Plotly doesn't have a direct way to plot a networkx Graph
        So, we scatter plot points, and draw lines between them  
    https://plotly.com/python/plotly-fundamentals/    
        Here is a description of plotly figures: https://plotly.com/python/figure-structure/ 
    more relevant taken from : https://stackoverflow.com/questions/51410283/how-to-efficiently-create-interactive-directed-network-graphs-with-arrows-on-p

    """
    original_name = original_name.lower()
    # compute shortest path to get to original node (unweighted distance)
    # uncomment spring_layout if you want basic force-relaxation of graph
    pos = nx.spring_layout(G, weight="weight")
    #pos = circular_layout_partially_fixed(G, original_name= original_name)
    if concentric_circle_graphing:
        pos = concentric_circles(G, original_name=original_name)
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    edge_trace = add_plotly_edge_trace(G)
    node_trace = add_plotly_node_trace(G, original_name)

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

    # Plot the nodes and edges, and if original name supplied, highlight the original name
    data = [edge_trace, node_trace]
    if node_trace_original:
        data.append(node_trace_original)
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            title=
            'Arxiv co-author exploration<br>[Click and drag to form a box to zoom. Double-click to zoom out]',
            titlefont_size=16,
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    fig.show()


# TODO - add - on-click functionality
def on_click():
    pass
    # https://plotly.com/python/click-events/
    # Open arxiv link to the user https://arxiv.org/search/?query=Alexandra+Chouldechova&searchtype=all&source=header


def graph(G, original_name=None, concentric_circle_graphing=False):
    #plot_weighted_graph(G)
    plot_plotly(G,
                original_name=original_name,
                concentric_circle_graphing=concentric_circle_graphing)
