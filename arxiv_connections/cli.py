#/usr/bin/env python3

import click
import logging
import pandas as pd
# locals
from arxiv_connections import (graphing, arxiv_util)

# TODO - save the authors and things optionally
# TODO - save the plot optionally
# TODO - consider different ways of sorting received articles

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
format = "%(asctime)s - %(levelname)s - %(message)s"
format = "%(levelname)s - %(message)s"
stream_handler.setFormatter(
    logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))

logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
logger = logging.getLogger()
# TODO - improve logging to not be so noisy all the time


@click.group(help=""" """)
@click.pass_context
def cli(ctx):
    """ TODO - check back in here,
    no need for sub-commands (as of right now)
    as I only have 1 cli command so far
    """
    return


@cli.command(name="crawl-and-plot",
             help="""crawl arxiv, create graph of co-authored connections""")
@click.argument("original_author",
                nargs=1,
                default="Mr. Rogers",
                required=True)
@click.option("--save-csv",
              "-s",
              default=None,
              show_default=True,
              required=False,
              help="""CSV to save article-crawl""")
@click.option("--read-csv",
              "-r",
              default=None,
              show_default=True,
              required=False,
              help="""CSV to read from (won't crawl arxiv directly then)""")
@click.option("--max-results-per-search",
              "-m",
              default=10,
              show_default=True,
              required=False,
              help="""How many articles to accept per author""")
@click.option("--max-depth",
              "-d",
              default=3,
              show_default=True,
              required=False,
              help="""max-depth to traverse if searching arxiv""")
@click.option(
    "--concentric-circle-graphing",
    "-c",
    default=False,
    show_default=True,
    is_flag=True,
    help=
    "visualize graph as a series of concentric circles, instead of force-directed"
)
@click.option(
    "--dont-halve-queries-per-graph-deepening",
    "-H",
    default=False,
    show_default=True,
    is_flag=True,
    help=
    "Default case: for each network-deepening, shrink the # of queries to scrape by 1/2. This flag turns this off"
)
@click.option("--debug_mode",
              "-D",
              default=False,
              show_default=True,
              is_flag=True,
              help="set logging to debug level")
@click.pass_context
def crawl_and_plot(ctx, original_author, save_csv, read_csv,
                   max_results_per_search, max_depth,
                   concentric_circle_graphing,
                   dont_halve_queries_per_graph_deepening, debug_mode):
    if debug_mode:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    if read_csv:
        articles = pd.read_csv(read_csv)
    else:
        articles = arxiv_util.BFS_author_query(
            original_author=original_author,
            max_search_results=max_results_per_search,
            halve_queries_by_depth=not dont_halve_queries_per_graph_deepening,
            max_depth=max_depth)
        if save_csv:
            articles.to_csv(save_csv)
    # generate a graph of authors, where the weight is the number of papers shared
    G = arxiv_util.generate_author_graph(articles)
    #plot_weighted_graph(G)
    graphing.graph(G,
                   original_author,
                   concentric_circle_graphing=concentric_circle_graphing)


# TODO - add in process for computing distance between 2 different people
# TODO - add in process for getting a report on recommendations of related authors


def main():
    cli()


if __name__ == "__main__":
    main()
