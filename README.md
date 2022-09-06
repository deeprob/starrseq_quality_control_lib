# Quality control of STARRSeq data

Deduplicated, aligned and filtered STARRSeq data was further examined to check ensure that the tested regions were well represented.

# STEPS

1. Check number of raw read, filtered reads, replicate-wise region coverage and depth.

2. Create a new mater list with regions that have atleast 50 reads per replicate for downstream analysis. The enhancer activity of these regions can be called with higher confidence.

3. Break the new master list into overlapping windows of size 500 bps and stride 50 bps.

4. Get merged depth of the overlapping windows.

# Output

1. Depth of regions of interest per library.

2. Filtered master list with regions that had atleast 50 reads assigned to it per replicate.

3. Depth of the overlapping windows in the filtered master list.

# Script descriptions

1. root/src/0_get_read_qc_stats.py: Reports quality control stats listed below.
2. root/src/1_create_filtered_master_list.py: Creates a new master list where each region had at least 50 reads for each replicate in the input library.
3. root/src/2_create_overlapping_windows.py: Breaks the master list into overlapping fragments of size 500 bp and stride 50 bp
4. root/src/3_get_window_depth.py: Calculates merged library coverage of the fragmented and filtered master list

# ReadQC Stats reported

## Region of Interest metrics

1. Number of regions
2. Mean length of regions
3. Total length of all regions

## Library Quality Control metrics

1. Number of raw reads
2. Number of filtered reads
3. Library coverage
4. Library depth
5. Library replicate correlation
