#!/bin/bash
GIT_HOME=$(git rev-parse --show-toplevel)
nbstripout $GIT_HOME/*/*ipynb
python -m yapf -i $GIT_HOME/*/*py
