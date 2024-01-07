#!/bin/bash

CWD=/home/nn/pattern-transformer
cd $CWD
# Activate conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate py310

# Set PYTHONPATH and run tests
export PYTHONPATH=$PYTHONPATH:/home/nn/pattern-transformer
timeout 86400 python database_tests/redis/TestRedis.py

# # Collect coverage data
# cd /home/nn/FalkorDB/bin/linux-x64-debug-cov/src
# lcov --capture --directory /home/nn/FalkorDB/bin/linux-x64-debug-cov/src --output-file /home/nn/FalkorDB/bin/linux-x64-debug-cov/coverage.info

# cd /home/nn/FalkorDB/bin/linux-x64-debug-cov
# # Generate HTML report
# [ -d out ] && mv out "$date"

# echo "fuckkk"
# pwd

# genhtml coverage.info --output-directory out
# echo "finish"

