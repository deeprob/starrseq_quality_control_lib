#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data5/deepro/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data5/deepro/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/data5/deepro/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/data5/deepro/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate starrseq

meta_file="/data5/deepro/starrseq/data/meta_data/metadata.json"
lib_name="input"
in_dir="/data5/deepro/starrseq/main_library/2_quality_control_lib/data"
store_dir="/data5/deepro/starrseq/main_library/2_quality_control_lib/data"

python /data5/deepro/starrseq/main_library/2_quality_control_lib/src/1_create_filtered_master_list.py $meta_file $lib_name $in_dir $store_dir
