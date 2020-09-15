#!/bin/bash
# apply python formatting to .py and .ipynb files
GIT_HOME=$(git rev-parse --show-toplevel)

files=`git diff --name-only --cached`

for filename in $files; do

# apply yapf on .py files
if [[ $filename == *.py ]] 
then
    python -m yapf -i $GIT_HOME/$filename
fi 

# clean the jupyter notebooks, to make sure that they don't bloat
if [[ $filename == *.ipynb ]] 
then
    nbstripout $GIT_HOME/$filename
fi 
# add all the changes to the commit
git add $GIT_HOME/$filename

done

