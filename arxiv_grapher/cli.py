#/usr/bin/env python3

import click
import logging
import pandas as pd
# locals
from arxiv_grapher import (graphing, arxiv_traverser)

# TODO - save the authors and things optionally
# TODO - save the plot optionally
# TODO - using logging library

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
format = "%(asctime)s - %(levelname)s - %(message)s"
format = "%(levelname)s - %(message)s"
stream_handler.setFormatter(
    logging.Formatter(format, datefmt="%Y-%m-%d %H:%M:%S"))

logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
logger = logging.getLogger()


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
@click.option("--debug_mode",
              "-d",
              default=False,
              show_default=True,
              is_flag=True,
              help="set logging to debug level")
@click.pass_context
def crawl_and_plot(ctx, original_author, save_csv, read_csv, debug_mode):
    if read_csv:
        articles = pd.read_csv(read_csv)
    else:
        articles = arxiv_traverser.BFS_author_query(
            original_author=original_author, max_search_results=5, max_depth=2)
    if save_csv:
        articles.to_csv(save_csv)
    # generate a graph of authors, where the weight is the number of papers shared
    G = arxiv_traverser.generate_author_graph(articles)
    #plot_weighted_graph(G)
    graphing.graph(G)


def main():
    cli()


if __name__ == "__main__":
    main()
