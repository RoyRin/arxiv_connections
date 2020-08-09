#!/bin/bash

nbstripout */*ipynb *ipynb
python -m yapf -i **/*py *py
