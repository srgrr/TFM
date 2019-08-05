#!/bin/bash

num_nodes=$1
num_experiments=$2
points_per_experiments=$3

enqueue_compss \
  --qos=debug \
  --num_nodes=$1 \
  --worker_working_dir=scratch \
  pycompss_vectorized.py $2 $3
