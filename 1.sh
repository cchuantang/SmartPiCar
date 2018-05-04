#!/bin/bash  
  
current_dir=$(pwd)  
python3dir=$(which python)   
  
mainfile=aws.py  
  
echo $current_dir  
echo $script_dir  
echo $python3dir  
echo "$python3dir $current_dir/$mainfile;"  
  
until $python3dir $current_dir/$mainfile; do  
    echo "Server $mainfile  crashed with exit code $?.  Respawning.." >&2  
    sleep 5  
done  
