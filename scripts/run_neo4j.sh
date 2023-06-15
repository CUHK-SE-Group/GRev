#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python database_tests/neo4j/TestNeo4j.py
