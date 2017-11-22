#!/bin/bash


p=$(echo "import os, sys;  print(os.path.abspath(sys.argv[0]))" | python)

# this doesn't work!!!
eval $(export PATH=$PATH:$p)


