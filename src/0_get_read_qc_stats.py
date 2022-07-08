import argparse
import utils as ut
from itertools import starmap


def main(
    input_data_dir,
    storage_dir,
    library_prefix, 
    library_replicates, 
    library_read_pairs,
    roi_file,
    library_short,
    debug=True
    ):
    # statistics_file
    stats_filepath = ut.get_statistics_filepath(storage_dir, library_short)
    stats_file = open(stats_filepath, "w")
    # roi statistics
    roi_num, roi_meansize, roi_total_bps = ut.get_roi_info(roi_file)
    stats_file.write(f"roi_stats,roi_num,{roi_num}\n")
    stats_file.write(f"roi_stats,roi_meansize,{roi_meansize}\n")
    stats_file.write(f"roi_stats,roi_total_bps,{roi_total_bps}\n")
    # raw data statistics
    raw_data_suff = ut.get_analyzed_filename_suffix("raw_data")
    raw_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, library_read_pairs, raw_data_suff)
    raw_data_filepaths = [ut.get_analyzed_filepaths(input_data_dir, "raw_data", library_short, fn) for fn in raw_data_filenames]
    raw_file_reads = ut.run_singleargs_pool_job(ut.get_num_reads_fastq, raw_data_filepaths)
    raw_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, raw_data_suff) for fn in raw_data_filenames]
    for rfn, rfr in zip(raw_data_filenames_parsed, raw_file_reads):
        stats_file.write(f"raw_reads,{rfn},{rfr}\n")
    # filtered data statistics
    filtered_data_suff = ut.get_analyzed_filename_suffix("filtered")
    filtered_data_filenames = ut.get_analyzed_filenames(library_prefix, library_replicates, "", filtered_data_suff)
    filtered_data_filepaths = [ut.get_analyzed_filepaths(input_data_dir, "filtered", library_short, fn) for fn in filtered_data_filenames]
    filtered_file_reads = ut.run_singleargs_pool_job(ut.get_num_reads_fastq, filtered_data_filepaths)
    filtered_data_filenames_parsed = [ut.remove_prefix_suffix(fn, library_prefix, filtered_data_suff) for fn in filtered_data_filenames]
    for ffn, ffr in zip(filtered_data_filenames_parsed, filtered_file_reads):
        stats_file.write(f"filtered_reads,{ffn},{ffr}\n")
    # library coverage
    coverage_iter = [(freads, roi_total_bps, 150, True) for freads in filtered_file_reads]
    filtered_files_coverage = list(starmap(ut.get_coverage, coverage_iter))
    for ffn, c in zip(filtered_data_filenames_parsed, filtered_files_coverage):
        stats_file.write(f"coverage,{ffn},{c}\n")
    stats_file.close()
    # library depth bed creation
    depth_bed_filepaths = list(starmap(ut.get_depth_bed_filepaths, [(storage_dir, library_short, library_prefix, rep) for rep in library_replicates.split()]))
    depth_iter = [(fp, roi_file, bo) for fp,bo in zip(filtered_data_filepaths, depth_bed_filepaths)]
    ut.run_multiargs_pool_job(ut.get_roi_depth, depth_iter)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="STARRSeq analysis")
    parser.add_argument("meta_file", type=str, help="The meta json filepath where library information is stored")
    parser.add_argument("lib", type=str, help="The library name as given in the meta file")
    parser.add_argument("input_dir", type=str, help="Input files dir")
    parser.add_argument("store_dir", type=str, help="Output files dir")  

    cli_args = parser.parse_args()
    lib_args = ut.create_args(cli_args.meta_file, cli_args.lib)

    main(
        cli_args.input_dir,
        cli_args.store_dir,
        lib_args.library_prefix, 
        lib_args.library_reps, 
        lib_args.library_pair,
        lib_args.roi_file,
        lib_args.library_short
    )
