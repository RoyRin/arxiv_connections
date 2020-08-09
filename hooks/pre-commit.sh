#!/bin/bash
GIT_HOME=$(git rev-parse --show-toplevel)
nbstripout $GIT_HOME/arxiv_traverser/*ipynb
python -m yapf -i $GIT_HOME/arxiv_traverser/*py
git add $GIT_HOME/arxiv_traverser/*py
git add $GIT_HOME/arxiv_traverser/*ipynb