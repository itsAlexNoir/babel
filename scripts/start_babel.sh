#!/bin/zsh
source ~/.zshrc
conda activate babel
DIRNAME=`dirname "$0"`
streamlit run ${DIRNAME}/../src/babel_viz.py
