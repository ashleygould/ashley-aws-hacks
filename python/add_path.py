#!/bin/bash


p=$(echo "import os, sys;  print(os.path.abspath(sys.argv[0]))" | python)

# these doesn't work!!!
export PATH=$PATH:$p
eval "PATH=$PATH:$p"


