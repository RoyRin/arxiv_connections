# Arxiv-Connections

Arxiv-connections is a python pkg, and provides a CLI (`arxiv-connector`) to find academics related to other academics
 based on closeness through arxiv co-authorings.


## High-level Goal

* Given a person, find the people who are most related to the things they work on

## More concrete Goals

1. Create a visualization of the authors that surround a particular individual
2. Not yet accomplished : produce a framework where one can provide a name,
 and it would generate a report of where to look.

## How to install

### Pre-install

As with all development, I recommend using a virtual environment to prevent dependency issues.
Python3 comes with `venv`, and `virtualenv` also works. This step is optional, but recommended:

1. Create a fresh python virtual environment. Which looks something like
    * `python3.7 -m venv my_env37` or `virtualenv --python=/usr/bin/python3.7 my_env37`
    * followed by `source my_evn37/bin/activate` to enter the environment
    (to leave this python environment, run `deactivate` at anytime)

### Install from PyPi

1. `pip install arxiv-connections`

### Install from Source

1. `git clone git@github.com:RoyRin/arxiv_connections.git` 
2. `cd arxiv_connections && poetry install arxiv_connections`

## How to Use

Once you have done the steps from 'How To Install', Now you can either run your own python package or use the CLI from terminal.

### High-level Description

There is 1 library (arxiv_connections) and 2 ways to use it: Command Line (call `arxiv-connector`) and calling the code directly 
from python (using `import arxiv_connection`). There is a jupyter notebook named arxiv_connections/arxiv_explorer.ipynb that 
is to serve as an example for this.

Generally, the current code will pull articles from Arxiv. It will generate graph-nodes for each author of each article. It 
will create edges between authors if they have co-authored something, with the edge weights proportional to the 
number of papers they have co-authored. 

For new author-investigations, you can scrape directly from arxiv. To make future investigations easier, you can
save the articles discovered off arxiv to a CSV, and then read from it in future iterations of the investigation.
(i.e. `arxiv-connector crawl-and-plot 'fname lastname' -s name.csv -m 7 -d 3` and 
then `arxiv-connector crawl-and-plot 'fname lastname' -r name.csv`)

**Note** you can easily make a lot of requests and keep the program from running. If you are 
pulling data from arxiv, you should estimate the number of you make as [max-results-per-search ** max-depth]. 

### Using the Command Line

If you have properly installed `arxiv-connector` it should tab-complete. Just calling it should produce a list of 
sub-commands. As of 8/10/20, there is only 1 sub-command `crawl-and-plot` to understand how it works, run
 `arxiv-connector crawl-and-plot --help`

### Quick-Start

**Quick-start from terminal:**

* Quick-start example #1 (from a file): `arxiv-connector crawl-and-plot 'dmitry rinberg' -r example_data/dmitry_rinberg.csv`
* Quick-start example #2 (pull from arxiv): `arxiv-connector crawl-and-plot 'dmitry rinberg' -s dmitry_rinberg_read.csv -d 3 -m 8 -D`
    (this example code is in the git repo)
* run `arxiv-connector --help` for an explanation of the CLI's commands

**Quick-start From Jupyter:**

* You can explore the data directly in a jupyter notebook using `arxiv_connector/arxiv_explorer.ipynb`
* To run the jupyter notebook, call `jupyter notebook` (you may need to `pip install jupyter`) and navigate to the jupyter file 

## Images

### crawl-and-plot

`arxiv-connector crawl-and-plot 'stuart russel' -m 15 -d 3`
![arxiv-connector crawl-and-plot 'stuart russel' -m 15 -d 3](https://github.com/RoyRin/arxiv_connections/blob/master/assets/screenshot_big_graph.png)
`arxiv-connector crawl-and-plot 'stuart russel' -m 7 -d 3`
![arxiv-connector crawl-and-plot 'stuart russel' -m 7 -d 3](https://github.com/RoyRin/arxiv_connections/blob/master/assets/screenshot_small_graph.png)
How to Zoom
![How to Zoom](https://github.com/RoyRin/arxiv_connections/blob/master/assets/screenshot_how_to_zoom.png)
Hover
![Hover](https://github.com/RoyRin/arxiv_connections/blob/master/assets/zoom_and_hover.png)


## Development

Note, this has been developed on Ubuntu 18.04.

### Testing

To test run `pytest tests`

### Formatting for developers
Commit hooks : following guidance from https://codeinthehole.com/tips/tips-for-using-a-git-pre-commit-hook/ and https://githooks.com/

1. To set-up easy formatting practices (i.e yapf + stripping jupyter notebooks):
    * run `ln -s ../../hooks/pre-commit.sh .git/hooks/pre-commit` from arxiv_connector home

## To-Do list

### Need To-Do

* Add tests !
* read through all the TODO comments, and actually fix them!

### Nice To-Do

* be able to create a metric between 2 different authors
* Investigate ways to define a few metrics on a graph, then rank individuals
* Generate reports on other academics, as a way to investigate who to look into next
* Be able to process more information than just Co-authoring, when considering new academics (i.e. topics)
* Add some images and put them in the git repo, for others to understand the tool better

* To-Do define some kind of bottle-neck distance or distance about number of paths to get to another individual
`(In order to avoid bottlenecks)

### Graphing To-Do

* Make the distance between nodes be porportional to the weight between them

