#!/bin/bash
#SBATCH --account=girirajan
#SBATCH --partition=girirajan
#SBATCH --job-name=starr_rqc
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=400:0:0
#SBATCH --mem-per-cpu=20G
#SBATCH --chdir /data5/deepro/starrseq/main_library/2_quality_control_lib/src
#SBATCH -o /data5/deepro/starrseq/main_library/2_quality_control_lib/slurm/logs/2_out.log
#SBATCH -e /data5/deepro/starrseq/main_library/2_quality_control_lib/slurm/logs/2_err.log
#SBATCH --nodelist qingyu

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

echo `date` starting job on $HOSTNAME
python /data5/deepro/starrseq/main_library/2_quality_control_lib/src/2_create_overlapping_windows.py $meta_file $lib_name $in_dir $store_dir
echo `date` ending job
