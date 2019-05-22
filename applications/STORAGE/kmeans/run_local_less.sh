#!/bin/bash -e

  # Define script variables
  scriptDir=$(dirname $0)
  execFile=src/kmeans.py
  appClasspath=${scriptDir}/src/
  appPythonpath=${scriptDir}/src/

  
  # Retrieve arguments
  tracing=$1

  # Leave the application args on $0
  shift 1

  # Launch the application
  runcompss \
  --pythonpath=$(pwd)/src \
  --tracing=$tracing \
  -t \
  -g \
  $(pwd)/src/kmeans.py $@
