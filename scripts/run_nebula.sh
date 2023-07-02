#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python database_tests/nebula/TestNebula.py
