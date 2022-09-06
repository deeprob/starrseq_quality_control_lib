import os
import pandas as pd
import argparse
import utils as ut


def main(
    input_data_dir,
    store_dir,
    window_file,
    lib_prefix,
    lib_replicates,
    lib_short,
    ):
    # get the bam file
    filtered_bam_file = os.path.join(input_data_dir, "filtered", lib_short, f"{lib_prefix}.bam")
    # depth out file
    store_file = os.path.join(store_dir, "window_depth", lib_short, f"{lib_prefix}.bed")
    os.makedirs(os.path.dirname(store_file), exist_ok=True)
    # create windows
    ut.get_roi_depth(filtered_bam_file, window_file, store_file)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("lib_name", type=str, help="The library name as given in the meta file")
    parser.add_argument("input_dir", type=str, help="Input files dir")
    parser.add_argument("store_dir", type=str, help="Output files dir")

    cli_args = parser.parse_args()
    lib_args = ut.create_args(cli_args.meta_file, cli_args.lib_name)

    main(
        cli_args.input_dir,
        cli_args.store_dir,
        lib_args.roi_window_file,
        lib_args.library_prefix, 
        lib_args.library_reps,
        lib_args.library_short        
    )