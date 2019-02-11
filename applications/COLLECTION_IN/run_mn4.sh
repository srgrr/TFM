#!/bin/bash

# Launch the two experiment applications in MN4
# As a reminder, MN4 works with a queue system
# This is why we are invoking these two applications with
# enqueue_compss


# Resources in master: create all resources in the master, send them as a first-time
# parameters to the task with the collection
enqueue_compss \
  --qos=debug \
  -dg \
  resources_in_master.py \


# Resources in worker: create all resources in the worker. This implies that the
# collection in parameter will have elements from various, different sources
# With 4 nodes we can be almost 100% sure that at we will have resources from
# different nodes in the select_element task
enqueue_compss \
  --qos=debug \
  --num_nodes=4 \
  --max_tasks_per_node=1 \
  -dg \
  resources_in_worker.py \
