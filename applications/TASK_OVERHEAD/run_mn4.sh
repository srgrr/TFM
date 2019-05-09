# Launch the main.py script as a mn4 job
# COMPSs is loaded as a module, so .bashrc must be
# modified to load different COMPSs versions
enqueue_compss \
  --qos=debug \
  --num_nodes=2 \
  --max_tasks_per_node=1 \
  -t \
  main.py \
