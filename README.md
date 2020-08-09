# Intro:
Arxiv-traverser is a python pkg, and provides a CLI to find academics related to other academics
 based on closeness through arxiv co-authorings.


## High-level Goal:
* Given a person, find the people who are most related to the things they work on

## More concrete Goals: 
1. Create a visualization of the authors that surround a particular individual
2. Not yet accomplished : produce a framework where one can provide a name,
 and it would generate a report of where to look 

## How to install:
1. `git clone git@github.com:RoyRin/arxiv_traverser.git` 
2. Create a fresh python virtual environment. Which looks something like 
    - `python3.7 -m venv my_env37` or `virtualenv --python=/usr/bin/python3.7 my_env37`
    - followed by `source my_evn37/bin/activate` to enter the environment
    - (to leave this python environment, run `deactivate` at anytime)
3. `cd arxiv_traverser && poetry install arxiv_traverser`

## How to Use:
Once you have done the steps from 'How To Install', Now you can either run your own python package or use the CLI from terminal
    - from terminal, 
        - Quick-start example: `arxiv-traverser crawl-and-plot 'dmitry rinberg' -r test_data/dmitry_rinberg.csv`
        - run `arxiv-traverser --help` for an explanation of how to run things
    - From Jupyter:
        - You can explore the data directly in a jupyter notebook using arxiv_traverser/arxiv_explorer.ipynb
        - To run the jupyter notebook, call `jupyter notebook` (you may need to `pip install jupyter`) and navigate to the jupyter file 

# Need To-Do:
- Add tests !
- read through all the TODO comments, and actually fix them!

# Nice To-Do:
- be able to create a metric between 2 different authors
- Investigate ways to define a few metrics on a graph, then rank individuals
- Generate reports on other academics, as a way to investigate who to look into next
- Be able to process more information than just Co-authoring, when considering new academics (i.e. topics)
- Add some images and put them in the git repo, for others to understand the tool better

- To-Do define some kind of bottle-neck distance or distance about number of paths to get to another individual
`(In order to avoid bottlenecks)
# Graphing To-Do:
- Make the distance between nodes be porportional to the weight between them
