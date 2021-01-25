#!/bin/bash
source ~/.bashrc
conda activate babel
DIRNAME=`dirname "$0"`
streamlit run ${DIRNAME}/../src/babel_viz.py -- --db_path ${DIRNAME}../databases
