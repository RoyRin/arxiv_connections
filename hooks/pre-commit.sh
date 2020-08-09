#!/bin/bash
GIT_HOME=$(git rev-parse --show-toplevel)
# clean the jupyter notebooks, to make sure that they don't bloat
nbstripout $GIT_HOME/arxiv_traverser/*ipynb
# apply yapf on python files
python -m yapf -i $GIT_HOME/arxiv_traverser/*py
# add all the changes to the commit
git add $GIT_HOME/arxiv_traverser/*py
git add $GIT_HOME/arxiv_traverser/*ipynb