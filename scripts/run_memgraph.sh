#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python database_tests/memgraph/TestMemGraph.py
