#! /bin/bash
tmp=`echo $(date +%Y-%m-%d)`
arg1="neores"

save_path=$arg1"/"$tmp
find $arg1 -maxdepth 1 -name "*.neo" -exec rm -rf {} \;
if [ -d $save_path ]; then
    rm -rf $save_path
fi
mkdir $save_path
./neodys_ephem.py $save_path


