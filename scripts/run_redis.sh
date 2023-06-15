#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python database_tests/redis/TestRedis.py
