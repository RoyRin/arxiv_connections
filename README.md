# Intro
Arxiv-traverser is a python pkg + CLI to find academics based on closeness through 
arxiv co-authorings.


## High-level Goals:
1. Given a person, find the people who are most related to the things they work on
2. create a visualization of the authors that surround a particular individual
3. Ideally, one can provide a name, and it would generate a report of where to look 

## How to install/get-started:
1. Create a python virtual environment. Which looks something like 
    - `python3.7 -m venv my_env37` or `virtualenv --python=/usr/bin/python3.7 my_env37`
    - followed by `source my_evn37/bin/activate`
2. `git clone git@github.com:RoyRin/arxiv_traverser.git`
3. `pip install poetry && poetry install arxiv_traverser`
4. Now you can either run your own python package or use the CLI from terminal
    - from terminal, run `arxiv-traverser --help` for an explanation of how to run things

# To-Do goals
- read through all the TODO comments, and actually fix them!
- be able to create a metric between 2 different authors
- Generate reports on other academics, as a way to investigate where to continue next
- Add tests !

## Things to look into: 
    Investigate ways to define a few metrics on a graph, then rank individuals


